import time
import mediapipe as mp

from mediapipe.tasks.python.components.containers import detections

MODEL_PATH = './models/efficientdet_lite0.tflite'

human_detector = None
result_human_detector = None

def save_result_human_detector(result: detections.DetectionResult, unused_output_image: mp.Image, timestamp_ms: int):
    global result_human_detector

    result_human_detector = result

def human_detector_init(running_mode: str):
    global human_detector

    BaseOptions = mp.tasks.BaseOptions
    ObjectDetector = mp.tasks.vision.ObjectDetector
    ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    base_options = BaseOptions(
        model_asset_path=MODEL_PATH,
        delegate=0 # 0 for CPU, 1 for GPU
    )

    if running_mode == 'LIVE_STREAM':
        options = ObjectDetectorOptions(
            base_options=base_options,
            display_names_locale='en',
            max_results=1,
            score_threshold=0.5,
            category_allowlist=['person'],
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=save_result_human_detector
        )
    elif running_mode == 'IMAGE':
        options = ObjectDetectorOptions(
            base_options=base_options,
            display_names_locale='en',
            max_results=1,
            score_threshold=0.5,
            category_allowlist=['person'],
            running_mode=VisionRunningMode.IMAGE
        )

    human_detector = ObjectDetector.create_from_options(options)

def get_bbox(image, running_mode: str):
    global result_human_detector

    x_min, y_min, x_max, y_max = 0, 0, 0, 0

    if running_mode == 'LIVE_STREAM':
        human_detector.detect_async(image, time.time_ns() // 1_000_000)
    elif running_mode == 'IMAGE':
        result_human_detector = human_detector.detect(image)

    if result_human_detector:
        for detection in result_human_detector.detections:
            if detection.categories[0].category_name == 'person':
                bounding_box = detection.bounding_box
                x_min = int(bounding_box.origin_x)
                y_min = int(bounding_box.origin_y)
                x_max = int(bounding_box.origin_x + bounding_box.width)
                y_max = int(bounding_box.origin_y + bounding_box.height)
                break  # 找到一个人就退出循环

    return x_min, y_min, x_max, y_max
