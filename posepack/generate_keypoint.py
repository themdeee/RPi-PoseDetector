import time
import posepack
import numpy as np
import mediapipe as mp

from typing import Mapping
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

MODEL_PATH = './models/pose_landmarker_heavy.task'

_POSE_LANDMARKS_LEFT = frozenset([
    PoseLandmark.LEFT_EYE_INNER, PoseLandmark.LEFT_EYE,
    PoseLandmark.LEFT_EYE_OUTER, PoseLandmark.LEFT_EAR, PoseLandmark.MOUTH_LEFT,
    PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW,
    PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_PINKY, PoseLandmark.LEFT_INDEX,
    PoseLandmark.LEFT_THUMB, PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE,
    PoseLandmark.LEFT_ANKLE, PoseLandmark.LEFT_HEEL,
    PoseLandmark.LEFT_FOOT_INDEX
])

_POSE_LANDMARKS_RIGHT = frozenset([
    PoseLandmark.RIGHT_EYE_INNER, PoseLandmark.RIGHT_EYE,
    PoseLandmark.RIGHT_EYE_OUTER, PoseLandmark.RIGHT_EAR,
    PoseLandmark.MOUTH_RIGHT, PoseLandmark.RIGHT_SHOULDER,
    PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_WRIST,
    PoseLandmark.RIGHT_PINKY, PoseLandmark.RIGHT_INDEX,
    PoseLandmark.RIGHT_THUMB, PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_KNEE,
    PoseLandmark.RIGHT_ANKLE, PoseLandmark.RIGHT_HEEL,
    PoseLandmark.RIGHT_FOOT_INDEX
])

keypoint_generator = None
result_keypoint_generator = None

def get_pose_landmarks_style(image) -> Mapping[int, DrawingSpec]:
    pose_landmark_style = {}
    left_spec = DrawingSpec(
        color=(0, 138, 255), thickness=posepack.get_thickness(image) * 2)
    right_spec = DrawingSpec(
        color=(231, 217, 0), thickness=posepack.get_thickness(image) * 2)
    for landmark in _POSE_LANDMARKS_LEFT:
        pose_landmark_style[landmark] = left_spec
    for landmark in _POSE_LANDMARKS_RIGHT:
        pose_landmark_style[landmark] = right_spec
    pose_landmark_style[PoseLandmark.NOSE] = DrawingSpec(
        color=(224, 224, 224), thickness=posepack.get_thickness(image) * 2)
    return pose_landmark_style

def save_result_keypoint_generator(result: PoseLandmarkerResult, unused_output_image: mp.Image, timestamp_ms: int):
    global result_keypoint_generator

    result_keypoint_generator = result

def keypoint_generator_init(running_mode: str):
    global keypoint_generator

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    base_options = BaseOptions(
        model_asset_path=MODEL_PATH,
        delegate=0 # 0 for CPU, 1 for GPU
    )

    if running_mode == 'LIVE_STREAM':
        options = PoseLandmarkerOptions(
            base_options=base_options,
            num_poses=1,
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=save_result_keypoint_generator
        )
    elif running_mode == 'IMAGE':
        options = PoseLandmarkerOptions(
            base_options=base_options,
            num_poses=1,
            running_mode=VisionRunningMode.IMAGE
        )
    
    keypoint_generator = PoseLandmarker.create_from_options(options)

def get_keypoint(image, running_mode: str, display_keypoints: bool = True):
    global result_keypoint_generator

    keypoints = []

    #在annotated_image上绘制关键点 不在image上绘制
    np_image = image.numpy_view()
    annotated_image = np.copy(np_image)

    if running_mode == 'LIVE_STREAM':
        keypoint_generator.detect_async(image, time.time_ns() // 1_000_000)
    elif running_mode == 'IMAGE':
        result_keypoint_generator = keypoint_generator.detect(image)

    if result_keypoint_generator:       
        for pose_landmarks in result_keypoint_generator.pose_landmarks:
            if display_keypoints:
                pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                pose_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                                    z=landmark.z) for landmark
                    in pose_landmarks
                ])

                mp.solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    pose_landmarks_proto,
                    mp.solutions.pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=get_pose_landmarks_style(np_image),
                    connection_drawing_spec=DrawingSpec(thickness=posepack.get_thickness(np_image))
                )
        
            for pose_landmark in pose_landmarks:
                x = int(pose_landmark.x * np_image.shape[1])
                y = int(pose_landmark.y * np_image.shape[0])
                visibility = pose_landmark.visibility
                presence = pose_landmark.presence
                keypoints.append((x, y, visibility, presence))
    
    return annotated_image, keypoints
