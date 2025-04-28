import math

DEBUG_MODE = True

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

def is_armcrossed(left_elbow, right_elbow, left_wrist, right_wrist):
    left_elbow_x, left_elbow_y, left_elbow_visibility, left_elbow_presence = left_elbow
    right_elbow_x, right_elbow_y, right_elbow_visibility, right_elbow_presence = right_elbow    
    left_wrist_x, left_wrist_y, left_wrist_visibility, left_wrist_presence = left_wrist
    right_wrist_x, right_wrist_y, right_wrist_visibility, right_wrist_presence = right_wrist

    lenth_left_wrist_to_left_elbow = math.dist([left_wrist_x, left_wrist_y], [left_elbow_x, left_elbow_y])
    lenth_left_wrist_to_right_elbow = math.dist([left_wrist_x, left_wrist_y], [right_elbow_x, right_elbow_y])
    lenth_right_wrist_to_left_elbow = math.dist([right_wrist_x, right_wrist_y], [left_elbow_x, left_elbow_y])
    lenth_right_wrist_to_right_elbow = math.dist([right_wrist_x, right_wrist_y], [right_elbow_x, right_elbow_y])
    
    min_presence = min(left_elbow_presence, right_elbow_presence,
                       left_wrist_presence, right_wrist_presence)
    
    if DEBUG_MODE:
        print("左腕到左肘距离: ", lenth_left_wrist_to_left_elbow)
        print("左腕到右肘距离: ", lenth_left_wrist_to_right_elbow)
        print("右腕到左肘距离: ", lenth_right_wrist_to_left_elbow)
        print("右腕到右肘距离: ", lenth_right_wrist_to_right_elbow)
        print("最小置信度: ", min_presence)

    if (left_wrist_y < right_elbow_y and
        right_wrist_y < left_elbow_y and
        lenth_left_wrist_to_right_elbow < lenth_left_wrist_to_left_elbow and
        lenth_right_wrist_to_left_elbow < lenth_right_wrist_to_right_elbow):

        return "Armcrossed", min_presence
    else:
        return "Unknown", min_presence

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
        print("左腰角度: ", angle_hip_left)
        print("右腰角度: ", angle_hip_right)
        print("左膝盖角度: ", angle_knee_left)
        print("右膝盖角度: ", angle_knee_right)
        print("特征点最小置信度:", min_presence)

    if (angle_hip_left > 90 and angle_hip_right > 90 and
        angle_knee_left > 150 and angle_knee_right > 150):

        return "Bow", min_presence
    else:
        return "Unknown", min_presence

def is_handsup_I():
    return "Handsup-I"

def is_handsup_T():
    return "Handsup-T"

def is_handsup_Y():
    return "Handsup-Y"

def is_kneel():
    return "Kneel"

def is_squart():
    return "Squat"

def get_pose_test(keypoints):
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

    pose, min_presence = is_bow(left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle)

    return pose

def get_pose(keypoints):
    """
    通过关键点判断人体的姿态
    :param keypoints: 关键点坐标和置信度，格式为 [(x1, y1, conf1), (x2, y2, conf2), ...]
    :return: 姿态类别： 'stand'（站立）, 'walk'（行走）, 'jump'（跳跃）, 'unknown'（未知）
    """

    # 如果关键点数量少于23个，直接返回'unknown'
    if len(keypoints) < 23:
        return 'Need more keypoints'

    # 定义一些关键点的索引（基于 MediaPipe 的关键点索引）
    left_ankle = keypoints[27]   # 左脚踝
    right_ankle = keypoints[28]  # 右脚踝
    left_knee = keypoints[25]    # 左膝盖
    right_knee = keypoints[26]   # 右膝盖
    left_hip = keypoints[23]     # 左髋关节
    right_hip = keypoints[24]    # 右髋关节

    left_shoulder = keypoints[11]  # 左肩膀
    right_shoulder = keypoints[12]  # 右肩膀
    left_elbow = keypoints[13]    # 左肘部
    right_elbow = keypoints[14]   # 右肘部
    left_index = keypoints[15]    # 左食指
    right_index = keypoints[16]   # 右食指

    if DEBUG_MODE:
        print("左脚踝:", left_ankle)
        print("右脚踝:", right_ankle)
        print("左膝盖:", left_knee)
        print("右膝盖:", right_knee)
        print("左髋关节:", left_hip)
        print("右髋关节:", right_hip)

        print("左肩膀:", left_shoulder)
        print("右肩膀:", right_shoulder)

    # 获取关键点的坐标和置信度
    left_ankle_x, left_ankle_y, left_ankle_visibility, left_ankle_presence = left_ankle
    right_ankle_x, right_ankle_y, right_ankle_visibility, right_ankle_presence = right_ankle
    left_knee_x, left_knee_y, left_knee_visibility, left_knee_presence = left_knee
    right_knee_x, right_knee_y, right_knee_visibility, right_knee_presence = right_knee
    left_hip_x, left_hip_y, left_hip_visibility, left_hip_presence = left_hip
    right_hip_x, right_hip_y, right_hip_visibility, right_hip_presence = right_hip

    left_shoulder_x, left_shoulder_y, left_shoulder_visibility, left_shoulder_presence = left_shoulder
    right_shoulder_x, right_shoulder_y, right_shoulder_visibility, right_shoulder_presence = right_shoulder
    left_elbow_x, left_elbow_y, left_elbow_visibility, left_elbow_presence = left_elbow
    right_elbow_x, right_elbow_y, right_elbow_visibility, right_elbow_presence = right_elbow
    left_index_x, left_index_y, left_index_visibility, left_index_presence = left_index
    right_index_x, right_index_y, right_index_visibility, right_index_presence = right_index

    # 计算膝盖关节之间的角度
    def calculate_knee_angle(knee, hip, ankle):
        # 计算两个向量的夹角
        vector1 = (knee[0] - hip[0], knee[1] - hip[1])
        vector2 = (ankle[0] - knee[0], ankle[1] - knee[1])

        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

        if magnitude1 * magnitude2 == 0:
            return 0

        cos_theta = dot_product / (magnitude1 * magnitude2)
        angle_rad = math.acos(cos_theta)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    # 简单的姿态判断逻辑
    if (left_ankle_presence > 0.3 and right_ankle_presence > 0.3) or True: # always true for testing
        # 在 OpenCV 坐标系中，y 坐标值越大，位置越低

        # 计算左脚角度
        knee_angle_left = calculate_knee_angle(left_knee, left_hip, left_ankle)
        # 计算右脚角度
        knee_angle_right = calculate_knee_angle(right_knee, right_hip, right_ankle)
        if DEBUG_MODE:
            print("左脚角度,", knee_angle_left)
            print("右脚角度,", knee_angle_right)

        hip_angle_left = calculate_knee_angle(left_shoulder, left_hip, left_ankle)
        hip_angle_right = calculate_knee_angle(right_shoulder, right_hip, right_ankle)

        if DEBUG_MODE:
            print("左髋关节角度,", hip_angle_left)
            print("右髋关节角度,", hip_angle_right)

        # 计算脚踝之间的距离
        ankle_distance = abs(left_ankle_x - right_ankle_x)
        # 计算膝盖之间的距离
        knee_distance = abs(left_knee_x - right_knee_x)
        if DEBUG_MODE:
            print("脚踝之间的距离,", ankle_distance)
            print("膝盖之间的距离,", knee_distance)

        distance_left_index_to_right_elbow = math.dist([left_index_x, left_index_y], [right_elbow_x, right_elbow_y])
        distance_left_index_to_left_elbow = math.dist([left_index_x, left_index_y], [left_elbow_x, left_elbow_y])
        distance_right_index_to_left_elbow = math.dist([right_index_x, right_index_y], [left_elbow_x, left_elbow_y])
        distance_right_index_to_right_elbow = math.dist([right_index_x, right_index_y], [right_elbow_x, right_elbow_y])

        if DEBUG_MODE:
            print("左食指到右肘部的距离:", distance_left_index_to_right_elbow)
            print("左食指到左肘部的距离:", distance_left_index_to_left_elbow)
            print("右食指到左肘部的距离:", distance_right_index_to_left_elbow)
            print("右食指到右肘部的距离:", distance_right_index_to_right_elbow)
            print("左食指的y坐标:", left_index_y)
            print("右食指的y坐标:", right_index_y)
            print("左肘部的y坐标:", left_elbow_y)
            print("右肘部的y坐标:", right_elbow_y)

        # 判断逻辑
        flag_0 = left_ankle_y > left_knee_y > left_hip_y and right_ankle_y > right_knee_y > right_hip_y
        flag_1 = knee_angle_left < 30 and knee_angle_right < 30
        flag_2 = ankle_distance > knee_distance * 1.5
        flag_3 = ankle_distance < knee_distance * 1.5

        flag_bow = hip_angle_left < 150 and hip_angle_right < 150 and knee_angle_left < 20 and knee_angle_right < 20
        # flag_kneel = hip_angle_left > 135 and hip_angle_right > 135 and (knee_angle_left < 45 or knee_angle_right < 45)
        flag_armfolding = left_index_y < right_elbow_y and right_index_y < left_elbow_y and distance_left_index_to_right_elbow < distance_left_index_to_left_elbow and distance_right_index_to_left_elbow < distance_right_index_to_right_elbow

        flag_stand = hip_angle_left > 150 and hip_angle_right > 150 

        flag_armopening = False

        '''
        如果命中多个条件，再使用置信度的平均值或方差来决定最终输出的姿态
        '''
        
        if flag_armfolding:
            return 'Armfolding'
        
        
        if flag_bow and not flag_stand:
            return 'Bow'
        
        # if flag_kneel:
        #     return 'Kneel'

        # 如果左脚踝和右脚踝的 y 坐标都大于膝盖和髋关节的 y 坐标，并且膝盖之间的角度小于一定阈值，判定为站立
        if flag_0 and flag_1 and flag_3 :
            return 'Stand'

        # 如果脚踝之间的距离大于膝盖之间的距离，判定为行走
        if flag_2:
            return 'Walk'

        # 如果左脚踝和右脚踝的 y 坐标都大于髋关节的 y 坐标，并且膝盖之间的角度大于一定阈值，判定为跳跃
        if left_ankle_y > left_hip_y and right_ankle_y > right_hip_y:
            if knee_angle_left > 60 or knee_angle_right > 60:  # 设置角度阈值为60度
                return 'Jump'

    # 如果以上条件都不满足，返回'unknown'
    return 'Unknown'
