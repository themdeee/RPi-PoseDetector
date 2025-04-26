import cv2

def get_fontscale(image):
    fontscale = (image.shape[0] + image.shape[1]) / 1280

    return fontscale

def get_thickness(image):
    thickness = max(1, int((image.shape[0] + image.shape[1]) / 540))

    return thickness

def get_original_image(image, fps=None, running_mode: str = "IMAGE"):
    # 显示帧率
    if running_mode == "IMAGE":
        image = image
    elif running_mode == "LIVE_STREAM":
        image = cv2.putText(
            image, 
            f"Camera FPS: {fps:.1f}", 
            (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            get_fontscale(image), 
            (0, 255, 0),  # 绿色
            get_thickness(image), 
            cv2.LINE_AA,
        )
    
    return image

def get_processed_image(image, bbox, pose, fps=None, running_mode: str = "IMAGE"):
    # 人体框选
    x_min, y_min, x_max, y_max = bbox
    image = cv2.rectangle(
        image, 
        (x_min, y_min),
        (x_max, y_max), 
        (0, 255, 0),  # 绿色
        get_thickness(image) 
    )
    
    # 标记姿势
    image = cv2.putText(
        image, 
        pose, 
        (x_min, y_min - 10), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        get_fontscale(image), 
        (0, 255, 0),  # 绿色
        get_thickness(image), 
        cv2.LINE_AA,
    )
    
    # 显示帧率
    if running_mode == "LIVE_STREAM" and fps is not None:
        image = cv2.putText(
            image, 
            f"Process FPS: {fps:.1f}", 
            (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            get_fontscale(image), 
            (0, 255, 0),  # 绿色
            get_thickness(image), 
            cv2.LINE_AA,
        )

    return image
