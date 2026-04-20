import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import threading
import time
import requests
import os
import queue

class SnakeGestureController:
    """
    Optimized gesture controller for Snake.
    Uses 'flick' detection (wrist tilt) rather than 'reaching' for lower latency.
    """
    def __init__(self, throttle=0.15):
        self.model_path = 'hand_landmarker.task'
        self._ensure_model_exists()
        self.detector = None
        self.cap = None
        self._initialize_resources()
        
        self.throttle = throttle
        self.last_move_time = 0
        self.move_queue = queue.Queue(maxsize=2)
        self.stop_event = threading.Event()
        self.thread = None

    def _initialize_resources(self):
        if self.detector is None:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.HandLandmarkerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.VIDEO,
                num_hands=1
            )
            self.detector = vision.HandLandmarker.create_from_options(options)
        
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            # Lower resolution for speed
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def _ensure_model_exists(self):
        if not os.path.exists(self.model_path):
            try:
                print(f"Downloading model to {self.model_path}...")
                url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(self.model_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                if os.path.exists(self.model_path):
                    os.remove(self.model_path)
                print(f"Error downloading model: {e}")
                raise

    def start(self):
        self.stop_event.clear()
        # Drain stale moves from previous run
        while not self.move_queue.empty():
            try:
                self.move_queue.get_nowait()
            except queue.Empty:
                break
        self._initialize_resources()
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            # Note: 1.0s timeout prevents indefinite hangs on restart.
            # If thread remains alive (stuck in cap.read()), cap.release() 
            # below may race, but daemon=True ensures cleanup on exit.
            self.thread.join(timeout=1.0)

        if self.detector:
            self.detector.close()
            self.detector = None

        if self.cap:
            self.cap.release()
            self.cap = None

        cv2.destroyAllWindows()

    def _run_loop(self):
        while not self.stop_event.is_set():
            success, frame = self.cap.read()
            if not success:
                time.sleep(0.01)
                continue

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
                        if dx > 0.1:
                            move = "RIGHT"
                        elif dx < -0.1:
                            move = "LEFT"
                    else:
                        if dy > 0.1:
                            move = "DOWN"
                        elif dy < -0.1:
                            move = "UP"
                    
                    if move:
                        try:
                            self.move_queue.put_nowait(move)
                        except queue.Full:
                            pass
                        self.last_move_time = now

            cv2.imshow('Snake CV', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    def get_move(self):
        try:
            return self.move_queue.get_nowait()
        except queue.Empty:
            return None
