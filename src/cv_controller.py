import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import threading
import time
import requests
import os
from collections import deque

class SnakeGestureController:
    """
    Optimized gesture controller for Snake.
    Uses 'flick' detection (wrist tilt) rather than 'reaching' for lower latency.
    """
    def __init__(self, throttle=0.15):
        self.model_path = 'hand_landmarker.task'
        self._ensure_model_exists()
        
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        self.cap = cv2.VideoCapture(0)
        # Lower resolution for speed
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        self.throttle = throttle
        self.last_move_time = 0
        self.move_queue = deque(maxlen=2)
        self.running = False
        self.thread = None

    def _ensure_model_exists(self):
        if not os.path.exists(self.model_path):
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            response = requests.get(url)
            with open(self.model_path, "wb") as f: f.write(response.content)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread: self.thread.join()
        self.detector.close()
        self.cap.release()

    def _run_loop(self):
        while self.running:
            success, frame = self.cap.read()
            if not success: continue

            frame = cv2.flip(frame, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            result = self.detector.detect_for_video(mp_image, int(time.time() * 1000))

            if result.hand_landmarks:
                # Use Wrist (0) and Middle MCP (9) to determine tilt
                wrist = result.hand_landmarks[0][0]
                mcp = result.hand_landmarks[0][9]
                
                dx = mcp.x - wrist.x
                dy = mcp.y - wrist.y
                
                now = time.time()
                if now - self.last_move_time > self.throttle:
                    move = None
                    if abs(dx) > abs(dy):
                        move = "RIGHT" if dx > 0.1 else "LEFT"
                    else:
                        move = "DOWN" if dy > 0.1 else "UP"
                    
                    if move:
                        self.move_queue.append(move)
                        self.last_move_time = now

            cv2.imshow('Snake CV', frame)
            if cv2.waitKey(1) & 0xFF == 27: break

    def get_move(self):
        return self.move_queue.popleft() if self.move_queue else None
