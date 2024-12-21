import threading

import cv2
import numpy as np
from loguru import logger


class Camera:

    def __init__(self, id: int = 0) -> None:

        self.cam = self.__init_cam(id)
        self.lock = threading.Lock()

    def __init_cam(self, id: int) -> cv2.VideoCapture:
        cam = cv2.VideoCapture(id)
        cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        cam.set(cv2.CAP_PROP_FOCUS, 360)
        cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
        cam.set(cv2.CAP_PROP_SHARPNESS, 125)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cam

    def get_frame(self) -> cv2.typing.MatLike:
        with self.lock:
            ret, frame = self.cam.read()
            if not ret:
                logger.error("Failed to read frame from camera.")
                return np.array([])

            return cv2.flip(frame, 1)

    def release(self) -> None:
        with self.lock:
            if self.cam.isOpened():
                self.cam.release()
