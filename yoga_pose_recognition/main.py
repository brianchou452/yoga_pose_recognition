import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions

VisionRunningMode = mp.tasks.vision.RunningMode

current_frame = None
current_mask_frame = None


def init_cam() -> cv2.VideoCapture:
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cam.set(cv2.CAP_PROP_FOCUS, 360)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
    cam.set(cv2.CAP_PROP_SHARPNESS, 125)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cam


def draw_landmarks_on_image(
    rgb_image: np.ndarray,
    detection_result: PoseLandmarkerResult,
) -> np.ndarray:
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                )
                for landmark in pose_landmarks
            ],
        )
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style(),
        )
    return annotated_image


# Create a pose landmarker instance with the live stream mode:
def print_result(
    result: PoseLandmarkerResult,
    output_image: mp.Image,
    timestamp_ms: int,
) -> None:
    global current_frame
    global current_mask_frame

    if result.segmentation_masks is not None and len(result.segmentation_masks) > 0:
        segmentation_mask = result.segmentation_masks[0].numpy_view()
        visualized_mask = (
            np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
        )
        current_mask_frame = visualized_mask
    current_frame = draw_landmarks_on_image(output_image.numpy_view(), result)


options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/pose_landmarker_full.task",
        # model_asset_buffer=bytes(40960),
        delegate=BaseOptions.Delegate.CPU,
    ),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,
    output_segmentation_masks=True,
)


def run() -> None:
    cam = init_cam()
    global current_frame
    global current_mask_frame
    timestamp = 0.0
    start_time_ms = round(time.time() * 1000)
    with PoseLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            flipped = cv2.flip(frame, 1)

            if current_frame is None:
                current_frame = flipped

            cv2.imshow("frame", current_frame)
            if current_mask_frame is not None:
                cv2.imshow("mask", current_mask_frame)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=flipped,
            )

            timestamp = round(time.time() * 1000) - start_time_ms
            landmarker.detect_async(mp_image, timestamp)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cam.release()
    cv2.destroyAllWindows()
