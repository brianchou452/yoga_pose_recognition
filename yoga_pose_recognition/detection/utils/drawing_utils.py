import json
from enum import Enum
from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np
from loguru import logger
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions.drawing_utils import DrawingSpec

from yoga_pose_recognition.detection.body_connections import BodyConnections
from yoga_pose_recognition.detection.models.pose import Pose, PoseData

_RED = (48, 48, 255)
_GREEN = (48, 255, 48)
_GRAY = (128, 128, 128)


class ConnectionsStyleAttribute(Enum):
    NORMAL = "normal"
    WRONG = "wrong"
    CORRECT = "correct"


_BODY_CONNECTION_STYLE = {
    ConnectionsStyleAttribute.NORMAL: DrawingSpec(
        color=_GRAY,
        thickness=2,
    ),
    ConnectionsStyleAttribute.CORRECT: DrawingSpec(
        color=_GREEN,
        thickness=2,
    ),
    ConnectionsStyleAttribute.WRONG: DrawingSpec(
        color=_RED,
        thickness=3,
    ),
}


class DrawingUtils:
    pose_data: dict[str, Pose] | None

    def __init__(self) -> None:
        self.pose_data = None
        self.load_pose_data()

    def load_pose_data(self) -> None:
        if self.pose_data is not None:
            logger.info("Pose data already loaded.")
        with Path("data/pose.json").open(mode="r") as f:
            contents = f.read()
            json_data = json.loads(contents)
            pose_data_raw = PoseData(**json_data)
            self.pose_data = {}
            for pose in pose_data_raw.poses:
                self.pose_data[pose.name] = pose

    def load_background_image(self, image_path: str) -> np.ndarray:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")
        h, w = image.shape[:2]
        target_w, target_h = 1280, 720
        aspect_ratio = w / h
        target_ratio = target_w / target_h

        if aspect_ratio > target_ratio:
            new_w = target_w
            new_h = int(new_w / aspect_ratio)
        else:
            new_h = target_h
            new_w = int(new_h * aspect_ratio)

        resized = cv2.resize(image, (new_w, new_h))

        bg = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        start_x = (target_w - new_w) // 2
        start_y = (target_h - new_h) // 2
        bg[start_y : start_y + new_h, start_x : start_x + new_w] = resized

        return bg

    def extract_xyz(
        self,
        tuple1: Tuple[int, int],
        tuple2: Tuple[int, int],
    ) -> Tuple[int, int, int]:
        # 找出重複的值
        common_value_set = set(tuple1).intersection(set(tuple2))

        if not common_value_set:
            raise ValueError("No common value found between the two tuples.")

        if len(common_value_set) != 1:
            raise ValueError("More than one common value found between the two tuples.")

        common_value = common_value_set.pop()

        # 去除重複的值
        unique_values = list(set(tuple1).union(set(tuple2)) - {common_value})

        if len(unique_values) != 2:
            raise ValueError("The unique values count is not equal to 2.")

        x, z = unique_values
        y = common_value

        return x, y, z

    def calculate_angle(
        self,
        point1: np.ndarray,
        point2: np.ndarray,
        point3: np.ndarray,
    ) -> float:
        vector1 = point1 - point2
        vector2 = point3 - point2
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        cosine_angle = np.dot(vector1, vector2) / (norm1 * norm2)
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)

    def get_pose_connections_style(
        self,
        pose_name: str,
        pose_landmarks_proto: landmark_pb2.NormalizedLandmarkList,
    ) -> Dict[Tuple[int, int], DrawingSpec]:
        connections_style = {}
        if self.pose_data is None:
            raise ValueError("Pose data is not loaded.")

        for angle in self.pose_data[pose_name].angles:
            connection1 = BodyConnections[angle.connection1].value
            connection2 = BodyConnections[angle.connection2].value

            try:
                x, y, z = self.extract_xyz(connection1, connection2)
            except ValueError:
                logger.warning(f"Common point not found for {angle}")
                continue

            point1 = np.array(
                [
                    pose_landmarks_proto.landmark[x].x,
                    pose_landmarks_proto.landmark[x].y,
                    # pose_landmarks_proto.landmark[x].z, # 立體空間的角度比較難定義姿勢，所以先關閉
                ],
            )
            point2 = np.array(
                [
                    pose_landmarks_proto.landmark[y].x,
                    pose_landmarks_proto.landmark[y].y,
                    # pose_landmarks_proto.landmark[y].z,
                ],
            )
            point3 = np.array(
                [
                    pose_landmarks_proto.landmark[z].x,
                    pose_landmarks_proto.landmark[z].y,
                    # pose_landmarks_proto.landmark[z].z,
                ],
            )
            calculated_angle = self.calculate_angle(point1, point2, point3)

            if abs(calculated_angle - angle.value) < 20:  # Allow some tolerance
                connections_style[connection1] = _BODY_CONNECTION_STYLE[
                    ConnectionsStyleAttribute.CORRECT
                ]
                connections_style[connection2] = _BODY_CONNECTION_STYLE[
                    ConnectionsStyleAttribute.CORRECT
                ]
            else:
                connections_style[connection1] = _BODY_CONNECTION_STYLE[
                    ConnectionsStyleAttribute.WRONG
                ]
                connections_style[connection2] = _BODY_CONNECTION_STYLE[
                    ConnectionsStyleAttribute.WRONG
                ]
                # logger.info(f"angle.connection1: {angle.connection1}")
                # logger.info(f"angle.connection2: {angle.connection2}")
                # logger.info(f"Calculated angle: {calculated_angle}")
                # logger.info(f"Expected angle: {angle.value}")

        for connection in BodyConnections:
            if connection.value not in connections_style:
                connections_style[connection.value] = _BODY_CONNECTION_STYLE[
                    ConnectionsStyleAttribute.NORMAL
                ]

        return connections_style
