from enum import Enum


class BodyConnections(Enum):
    # Face connections
    NOSE_TO_LEFT_EYE_INNER = (0, 1)
    LEFT_EYE_INNER_TO_LEFT_EYE = (1, 2)
    LEFT_EYE_TO_LEFT_EYE_OUTER = (2, 3)
    LEFT_EYE_OUTER_TO_LEFT_EAR = (3, 7)
    NOSE_TO_RIGHT_EYE_INNER = (0, 4)
    RIGHT_EYE_INNER_TO_RIGHT_EYE = (4, 5)
    RIGHT_EYE_TO_RIGHT_EYE_OUTER = (5, 6)
    RIGHT_EYE_OUTER_TO_RIGHT_EAR = (6, 8)
    NOSE_TO_LEFT_EAR = (0, 7)
    NOSE_TO_RIGHT_EAR = (0, 8)
    MOUTH_LEFT_TO_MOUTH_RIGHT = (9, 10)

    # Torso connections
    LEFT_SHOULDER_TO_RIGHT_SHOULDER = (11, 12)
    LEFT_SHOULDER_TO_LEFT_HIP = (11, 23)
    RIGHT_SHOULDER_TO_RIGHT_HIP = (12, 24)
    LEFT_HIP_TO_RIGHT_HIP = (23, 24)

    # Left arm connections
    LEFT_SHOULDER_TO_LEFT_ELBOW = (11, 13)
    LEFT_ELBOW_TO_LEFT_WRIST = (13, 15)
    LEFT_WRIST_TO_LEFT_PINKY = (15, 17)
    LEFT_WRIST_TO_LEFT_INDEX = (15, 19)
    LEFT_WRIST_TO_LEFT_THUMB = (15, 21)
    LEFT_PINKY_TO_LEFT_INDEX = (17, 19)

    # Right arm connections
    RIGHT_SHOULDER_TO_RIGHT_ELBOW = (12, 14)
    RIGHT_ELBOW_TO_RIGHT_WRIST = (14, 16)
    RIGHT_WRIST_TO_RIGHT_PINKY = (16, 18)
    RIGHT_WRIST_TO_RIGHT_INDEX = (16, 20)
    RIGHT_WRIST_TO_RIGHT_THUMB = (16, 22)
    RIGHT_PINKY_TO_RIGHT_INDEX = (18, 20)

    # Left leg connections
    LEFT_HIP_TO_LEFT_KNEE = (23, 25)
    LEFT_KNEE_TO_LEFT_ANKLE = (25, 27)
    LEFT_ANKLE_TO_LEFT_HEEL = (27, 29)
    LEFT_ANKLE_TO_LEFT_FOOT_INDEX = (27, 31)
    LEFT_FOOT = (29, 31)

    # Right leg connections
    RIGHT_HIP_TO_RIGHT_KNEE = (24, 26)
    RIGHT_KNEE_TO_RIGHT_ANKLE = (26, 28)
    RIGHT_ANKLE_TO_RIGHT_HEEL = (28, 30)
    RIGHT_ANKLE_TO_RIGHT_FOOT_INDEX = (28, 32)
    RIGHT_FOOT = (30, 32)
