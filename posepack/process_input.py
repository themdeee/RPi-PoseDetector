import cv2
import time
import posepack
import numpy as np
import mediapipe as mp

flag_inited_image = False
flag_inited_live_stream = False

time_last_input, time_last_process = 0, 0
counter_input, counter_process = 0, 0
fps_input, fps_process = 0, 0
keypoints_last = None

counter_skip_webcam, counter_skip_usbcam = 0, 0
image_output_last = None

def get_image(image):
    global flag_inited_image, flag_inited_live_stream

    if image is None:
        return None
    
    image = np.array(image)

    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)

    if not flag_inited_image:
        posepack.keypoint_generator_init('IMAGE')
        posepack.human_detector_init('IMAGE')

        flag_inited_image = True
        flag_inited_live_stream = False

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    bbox = posepack.get_bbox(image, 'IMAGE')

    if posepack.vars.flag_keypoints:
        image, keypoints = posepack.get_keypoint(image, 'IMAGE')
    else:
        image, keypoints = posepack.get_keypoint(image, 'IMAGE', False)

    pose = posepack.get_pose(keypoints)

    if bbox:
        image = posepack.get_processed_image(image, bbox, pose, 'IMAGE')
    
    return image

def get_webcam(image_input):
    global flag_inited_image, flag_inited_live_stream
    global time_last_input, time_last_process, counter_input, counter_process, fps_input, fps_process, keypoints_last
    global counter_skip_webcam, image_output_last

    if image_input is None:
        return None

    if posepack.vars.rotate == 90:
        image_input = cv2.rotate(image_input, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif posepack.vars.rotate == 180:
        image_input = cv2.rotate(image_input, cv2.ROTATE_180)
    elif posepack.vars.rotate == 270:
        image_input = cv2.rotate(image_input, cv2.ROTATE_90_CLOCKWISE)
    else:
        image_input = image_input

    if not flag_inited_live_stream:
        posepack.keypoint_generator_init('LIVE_STREAM')
        posepack.human_detector_init('LIVE_STREAM')

        flag_inited_image = False
        flag_inited_live_stream = True

    image_input = np.array(image_input)

    if image_input.shape[2] == 4:
        image_input = cv2.cvtColor(image_input, cv2.COLOR_RGBA2RGB)
    elif image_input.shape[2] == 3:
        image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)

    if image_input.dtype != np.uint8:
        image_input = (image_input * 255).astype(np.uint8)

    image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)

    counter_skip_webcam = (counter_skip_webcam + 1) % posepack.vars.frame
    process_this_frame = (counter_skip_webcam == 0)
    if process_this_frame:
        image_output = image_input.copy()
    else:
        image_output = image_output_last

    # 这种计算帧率方式会使结果帧率大于实际帧率 因为前后时间间隔大于1秒
    counter_input += 1
    time_now_input = time.time()
    if time_now_input - time_last_input >= 1.0:
        fps_input = counter_input
        counter_input = 0
        time_last_input = time_now_input
    
    image_input = posepack.get_original_image(image_input, fps_input, 'LIVE_STREAM')

    if process_this_frame:
        counter_skip_webcam = 0
        
        image_output = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_output)

        bbox = posepack.get_bbox(image_output, 'LIVE_STREAM')

        if posepack.vars.flag_keypoints:
            image_output, keypoints = posepack.get_keypoint(image_output, 'LIVE_STREAM')
        else:
            image_output, keypoints = posepack.get_keypoint(image_output, 'LIVE_STREAM', False)

        pose = posepack.get_pose(keypoints)

        if keypoints_last is not None and not np.array_equal(keypoints, keypoints_last):
            counter_process += 1
        keypoints_last = keypoints

        time_now_process = time.time()
        if time_now_process - time_last_process >= 1.0:
            fps_process = counter_process
            counter_process = 0
            time_last_process = time_now_process

        if bbox:
            image_output = posepack.get_processed_image(image_output, bbox, pose, fps_process, 'LIVE_STREAM')
        
        image_output_last = image_output

    return image_input, image_output

def get_usbcam():
    global flag_inited_image, flag_inited_live_stream
    global time_last_input, time_last_process, counter_input, counter_process, fps_input, fps_process, keypoints_last
    global counter_skip_usbcam, image_output_last

    if not flag_inited_live_stream:
        posepack.keypoint_generator_init('LIVE_STREAM')
        posepack.human_detector_init('LIVE_STREAM')
        
        flag_inited_image = False
        flag_inited_live_stream = True
    
    if posepack.vars.flag_button_usbcam:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Check usbcam connection")
            yield None, None

        cap.set(cv2.CAP_PROP_FPS, 60)

        if posepack.vars.resolution == 360:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        elif posepack.vars.resolution == 540:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        elif posepack.vars.resolution == 720:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        else:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        while cap.isOpened() and posepack.vars.flag_button_usbcam:
            success, image_input = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                break

            if posepack.vars.flag_flip:
                image_input = cv2.flip(image_input, 1)

            if posepack.vars.rotate == 90:
                image_input = cv2.rotate(image_input, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif posepack.vars.rotate == 180:
                image_input = cv2.rotate(image_input, cv2.ROTATE_180)
            elif posepack.vars.rotate == 270:
                image_input = cv2.rotate(image_input, cv2.ROTATE_90_CLOCKWISE)
            else:
                image_input = image_input

            image_input = np.array(image_input)

            if image_input.shape[2] == 4:
                image_input = cv2.cvtColor(image_input, cv2.COLOR_RGBA2RGB)
            elif image_input.shape[2] == 3:
                image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)

            if image_input.dtype != np.uint8:
                image_input = (image_input * 255).astype(np.uint8)

            counter_skip_usbcam = (counter_skip_usbcam + 1) % posepack.vars.frame
            process_this_frame = (counter_skip_usbcam == 0)
            if process_this_frame:
                image_output = image_input.copy()
            else:
                image_output = image_output_last

            counter_input += 1
            time_now_input = time.time()
            if time_now_input - time_last_input >= 1.0:
                fps_input = counter_input
                counter_input = 0
                time_last_input = time_now_input

            image_input = posepack.get_original_image(image_input, fps_input, 'LIVE_STREAM')

            if process_this_frame:
                counter_skip_usbcam = 0

                image_output = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_output)

                bbox = posepack.get_bbox(image_output, 'LIVE_STREAM')

                if posepack.vars.flag_keypoints:
                    image_output, keypoints = posepack.get_keypoint(image_output, 'LIVE_STREAM')
                else:
                    image_output, keypoints = posepack.get_keypoint(image_output, 'LIVE_STREAM', False)

                pose = posepack.get_pose(keypoints)

                if keypoints_last is not None and not np.array_equal(keypoints, keypoints_last):
                    counter_process += 1
                keypoints_last = keypoints

                time_now_process = time.time()
                if time_now_process - time_last_process >= 1.0:
                    fps_process = counter_process
                    counter_process = 0
                    time_last_process = time_now_process

                if bbox:
                    image_output = posepack.get_processed_image(image_output, bbox, pose, fps_process, 'LIVE_STREAM')

                image_output_last = image_output            
                        
            yield image_input, image_output
        else:
            cap.release()
            yield None, None
