import math

DEBUG_MODE = False

def get_angle(vertex, point1, point2):
    vector1 = (point1[0] - vertex[0], point1[1] - vertex[1])
    vector2 = (point2[0] - vertex[0], point2[1] - vertex[1])

    length1 = math.hypot(vector1[0], vector1[1])
    length2 = math.hypot(vector2[0], vector2[1])
    if length1 == 0 or length2 == 0:
        return 0.0

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    cos_angle = dot_product / (length1 * length2)
    cos_angle = max(min(cos_angle, 1.0), -1.0)
    angle = math.degrees(math.acos(cos_angle))
    
    return angle

def get_length(point1, point2):
    length = math.hypot(point1[0] - point2[0], point1[1] - point2[1])

    return length

def is_armcrossed(left_elbow, right_elbow, left_wrist, right_wrist):
    left_elbow_x, left_elbow_y, left_elbow_visibility, left_elbow_presence = left_elbow
    right_elbow_x, right_elbow_y, right_elbow_visibility, right_elbow_presence = right_elbow    
    left_wrist_x, left_wrist_y, left_wrist_visibility, left_wrist_presence = left_wrist
    right_wrist_x, right_wrist_y, right_wrist_visibility, right_wrist_presence = right_wrist

    length_left_wrist_to_left_elbow = get_length(left_wrist, left_elbow)
    length_left_wrist_to_right_elbow = get_length(left_wrist, right_elbow)
    length_right_wrist_to_left_elbow = get_length(right_wrist, left_elbow)
    length_right_wrist_to_right_elbow = get_length(right_wrist, right_elbow)
    
    min_presence = min(left_elbow_presence, right_elbow_presence,
                       left_wrist_presence, right_wrist_presence)
    
    if DEBUG_MODE:
        print("Armcrossed: ")
        print("左腕到左肘距离: ", length_left_wrist_to_left_elbow)
        print("左腕到右肘距离: ", length_left_wrist_to_right_elbow)
        print("右腕到左肘距离: ", length_right_wrist_to_left_elbow)
        print("右腕到右肘距离: ", length_right_wrist_to_right_elbow)
        print("最小置信度: ", min_presence)

    if (left_wrist_y < right_elbow_y and
        right_wrist_y < left_elbow_y and
        length_left_wrist_to_right_elbow < length_left_wrist_to_left_elbow and
        length_right_wrist_to_left_elbow < length_right_wrist_to_right_elbow and
        min_presence > 0.3):

        return "Armcrossed", min_presence
    else:
        return "", 0

def is_bow(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle):
    left_shoulder_x, left_shoulder_y, left_shoulder_visibility, left_shoulder_presence = left_shoulder
    right_shoulder_x, right_shoulder_y, right_shoulder_visibility, right_shoulder_presence = right_shoulder
    left_hip_x, left_hip_y, left_hip_visibility, left_hip_presence = left_hip
    right_hip_x, right_hip_y, right_hip_visibility, right_hip_presence = right_hip
    left_knee_x, left_knee_y, left_knee_visibility, left_knee_presence = left_knee
    right_knee_x, right_knee_y, right_knee_visibility, right_knee_presence = right_knee
    left_ankle_x, left_ankle_y, left_ankle_visibility, left_ankle_presence = left_ankle
    right_ankle_x, right_ankle_y, right_ankle_visibility, right_ankle_presence = right_ankle

    angle_hip_left = get_angle(left_hip, left_shoulder, left_ankle)
    angle_hip_right = get_angle(right_hip, right_shoulder, right_ankle)
    angle_knee_left = get_angle(left_knee, left_hip, left_ankle)
    angle_knee_right = get_angle(right_knee, right_hip, right_ankle)

    min_presence = min(left_shoulder_presence, right_shoulder_presence,
                       left_hip_presence, right_hip_presence,
                       left_knee_presence, right_knee_presence,
                       left_ankle_presence, right_ankle_presence)
    
    if DEBUG_MODE:
        print("Bow: ")
        print("左髋关节角度: ", angle_hip_left)
        print("右髋关节角度: ", angle_hip_right)
        print("左膝关节角度: ", angle_knee_left)
        print("右膝关节角度: ", angle_knee_right)
        print("特征点最小置信度:", min_presence)

    if (angle_hip_left > 90 and angle_hip_right > 90 and
        angle_hip_left < 130 and angle_hip_right < 130 and
        angle_knee_left > 150 and angle_knee_right > 150 and
        min_presence > 0.3):

        return "Bow", min_presence
    else:
        return "", 0

def is_handsup(nose, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle):
    nose_x, nose_y, nose_visibility, nose_presence = nose
    left_shoulder_x, left_shoulder_y, left_shoulder_visibility, left_shoulder_presence = left_shoulder
    right_shoulder_x, right_shoulder_y, right_shoulder_visibility, right_shoulder_presence = right_shoulder
    left_elbow_x, left_elbow_y, left_elbow_visibility, left_elbow_presence = left_elbow
    right_elbow_x, right_elbow_y, right_elbow_visibility, right_elbow_presence = right_elbow
    left_wrist_x, left_wrist_y, left_wrist_visibility, left_wrist_presence = left_wrist
    right_wrist_x, right_wrist_y, right_wrist_visibility, right_wrist_presence = right_wrist
    left_hip_x, left_hip_y, left_hip_visibility, left_hip_presence = left_hip
    right_hip_x, right_hip_y, right_hip_visibility, right_hip_presence = right_hip
    left_knee_x, left_knee_y, left_knee_visibility, left_knee_presence = left_knee
    right_knee_x, right_knee_y, right_knee_visibility, right_knee_presence = right_knee
    left_ankle_x, left_ankle_y, left_ankle_visibility, left_ankle_presence = left_ankle
    right_ankle_x, right_ankle_y, right_ankle_visibility, right_ankle_presence = right_ankle

    x1, y1 = left_shoulder_x, left_shoulder_y
    x2, y2 = left_wrist_x, left_wrist_y
    x3, y3 = right_shoulder_x, right_shoulder_y
    x4, y4 = right_wrist_x, right_wrist_y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator != 0:
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
        angle_arm = get_angle((px, py), (left_shoulder_x, left_shoulder_y), (right_shoulder_x, right_shoulder_y))
    else:
        angle_arm = 0.0

    angle_hip_left = get_angle(left_hip, left_shoulder, left_ankle)
    angle_hip_right = get_angle(right_hip, right_shoulder, right_ankle)
    angle_elbow_left = get_angle(left_elbow, left_shoulder, left_wrist)
    angle_elbow_right = get_angle(right_elbow, right_shoulder, right_wrist)

    # min_presence = min(nose_presence,
    #                    left_shoulder_presence, right_shoulder_presence,
    #                    left_elbow_presence, right_elbow_presence,
    #                    left_wrist_presence, right_wrist_presence,
    #                    left_hip_presence, right_hip_presence,
    #                    left_knee_presence, right_knee_presence,
    #                    left_ankle_presence, right_ankle_presence)
    
    min_presence = min(nose_presence,
                       left_shoulder_presence, right_shoulder_presence,
                       left_elbow_presence, right_elbow_presence,
                       left_wrist_presence, right_wrist_presence)

    if DEBUG_MODE:
        print("Handsup: ")
        print("手臂夹角: ", angle_arm)
        print("左髋关节角度: ", angle_hip_left)
        print("右髋关节角度: ", angle_hip_right)
        print("左肘关节角度: ", angle_elbow_left)
        print("右肘关节角度: ", angle_elbow_right)
        print("特征点最小置信度:", min_presence)

    is_armoverhead = left_wrist_y < nose_y and right_wrist_y < nose_y
    is_handsup = angle_elbow_left > 150 and angle_elbow_right > 150

    # if (angle_hip_left > 150 and angle_hip_right > 150 and is_handsup and min_presence > 0.3):
    if (is_handsup and min_presence > 0.3):
        if (angle_arm < 40 and is_armoverhead):
            return "Handsup-I", min_presence
        elif (angle_arm > 40 and angle_arm < 100 and is_armoverhead):
            return "Handsup-Y", min_presence
        elif (angle_arm > 100):
            return "Handsup-T", min_presence
        else:
            return "", 0
    else:
        return "", 0

def is_kneel(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle):
    left_shoulder_x, left_shoulder_y, left_shoulder_visibility, left_shoulder_presence = left_shoulder
    right_shoulder_x, right_shoulder_y, right_shoulder_visibility, right_shoulder_presence = right_shoulder
    left_hip_x, left_hip_y, left_hip_visibility, left_hip_presence = left_hip
    right_hip_x, right_hip_y, right_hip_visibility, right_hip_presence = right_hip
    left_knee_x, left_knee_y, left_knee_visibility, left_knee_presence = left_knee
    right_knee_x, right_knee_y, right_knee_visibility, right_knee_presence = right_knee
    left_ankle_x, left_ankle_y, left_ankle_visibility, left_ankle_presence = left_ankle
    right_ankle_x, right_ankle_y, right_ankle_visibility, right_ankle_presence = right_ankle

    angle_hip_left = get_angle(left_hip, left_shoulder, left_knee)
    angle_hip_right = get_angle(right_hip, right_shoulder, right_knee)
    angle_knee_left = get_angle(left_knee, left_hip, left_ankle)
    angle_knee_right = get_angle(right_knee, right_hip, right_ankle)

    min_presence = min(left_shoulder_presence, right_shoulder_presence,
                       left_hip_presence, right_hip_presence,
                       left_knee_presence, right_knee_presence,
                       left_ankle_presence, right_ankle_presence)
    
    if DEBUG_MODE:
        print("Kneel: ")
        print("左髋关节角度: ", angle_hip_left)
        print("右髋关节角度: ", angle_hip_right)
        print("左膝关节角度: ", angle_knee_left)
        print("右膝关节角度: ", angle_knee_right)
        print("特征点最小置信度:", min_presence)

    if (angle_hip_left > 120 and angle_hip_right > 120 and
        angle_knee_left < 60 and angle_knee_right < 60 and
        min_presence > 0.3):

        return "Kneel", min_presence
    else:
        return "", 0

def is_squart(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle):
    left_shoulder_x, left_shoulder_y, left_shoulder_visibility, left_shoulder_presence = left_shoulder
    right_shoulder_x, right_shoulder_y, right_shoulder_visibility, right_shoulder_presence = right_shoulder
    left_hip_x, left_hip_y, left_hip_visibility, left_hip_presence = left_hip
    right_hip_x, right_hip_y, right_hip_visibility, right_hip_presence = right_hip
    left_knee_x, left_knee_y, left_knee_visibility, left_knee_presence = left_knee
    right_knee_x, right_knee_y, right_knee_visibility, right_knee_presence = right_knee
    left_ankle_x, left_ankle_y, left_ankle_visibility, left_ankle_presence = left_ankle
    right_ankle_x, right_ankle_y, right_ankle_visibility, right_ankle_presence = right_ankle

    angle_hip_left = get_angle(left_hip, left_shoulder, left_knee)
    angle_hip_right = get_angle(right_hip, right_shoulder, right_knee)
    angle_knee_left = get_angle(left_knee, left_hip, left_ankle)
    angle_knee_right = get_angle(right_knee, right_hip, right_ankle)

    min_presence = min(left_shoulder_presence, right_shoulder_presence,
                       left_hip_presence, right_hip_presence,
                       left_knee_presence, right_knee_presence,
                       left_ankle_presence, right_ankle_presence)
    
    if DEBUG_MODE:
        print("Squart: ")
        print("左髋关节角度: ", angle_hip_left)
        print("右髋关节角度: ", angle_hip_right)
        print("左膝关节角度: ", angle_knee_left)
        print("右膝关节角度: ", angle_knee_right)
        print("特征点最小置信度:", min_presence)

    if (angle_hip_left < 120 and angle_hip_right < 120 and
        angle_knee_left < 90 and angle_knee_right < 90 and
        min_presence > 0.3):

        return "Squart", min_presence
    else:
        return "", 0

def get_pose(keypoints):
    if not isinstance(keypoints, list) or len(keypoints) < 33:
        return "Unknown"
    else:
        nose = keypoints[0]
        left_eye_inner = keypoints[1]
        left_eye = keypoints[2]
        left_eye_outer = keypoints[3]
        right_eye_inner = keypoints[4]
        right_eye = keypoints[5]
        right_eye_outer = keypoints[6]
        left_ear = keypoints[7]
        right_ear = keypoints[8]
        mouth_left = keypoints[9]
        mouth_right = keypoints[10]
        left_shoulder = keypoints[11]
        right_shoulder = keypoints[12]
        left_elbow = keypoints[13]
        right_elbow = keypoints[14]
        left_wrist = keypoints[15]
        right_wrist = keypoints[16]
        left_pinky = keypoints[17]
        right_pinky = keypoints[18]
        left_index = keypoints[19]
        right_index = keypoints[20]
        left_thumb = keypoints[21]
        right_thumb = keypoints[22]
        left_hip = keypoints[23]
        right_hip = keypoints[24]
        left_knee = keypoints[25]
        right_knee = keypoints[26]
        left_ankle = keypoints[27]
        right_ankle = keypoints[28]
        left_heel = keypoints[29]
        right_heel = keypoints[30]
        left_foot_index = keypoints[31]
        right_foot_index = keypoints[32]

        pose_armcrossed, presence_armcrossed = is_armcrossed(left_elbow, right_elbow, left_wrist, right_wrist)
        pose_bow, presence_bow = is_bow(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle)
        pose_kneel, presence_kneel = is_kneel(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle) 
        pose_squart, presence_squart = is_squart(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle)
        pose_handsup, presence_handsup = is_handsup(nose, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle)

        poses = [
            (pose_armcrossed, presence_armcrossed),
            (pose_bow, presence_bow),
            (pose_kneel, presence_kneel),
            (pose_squart, presence_squart),
            (pose_handsup, presence_handsup)
        ]
        
        poses_valid = [p for p in poses if p[0]]
        if not poses_valid:
            return "Unknown"
        
        pose_best = max(poses_valid, key=lambda x: x[1])

        if DEBUG_MODE:
            print("Best pose: ", pose_best[0])

        return pose_best[0]
