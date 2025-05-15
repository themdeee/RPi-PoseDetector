import gradio as gr
import posepack

webcam_constraints_360P = {
    "video": {
        "width": {"ideal": 640},
        "height": {"ideal": 360},
    },
}

webcam_constraints_540P = {
    "video": {
        "width": {"ideal": 960},
        "height": {"ideal": 540},
    },
}

webcam_constraints_720P = {
    "video": {
        "width": {"ideal": 1280},
        "height": {"ideal": 720},
    },
}

'''
当前顺序：
1. usbcam输入 2. usbcam按钮
3. webcam输入 
4. image输入 5. image按钮
6. image输出
7. resolution下拉框 8. rotate下拉框
9. flip选择框 10. keypoints选择框
11.checkbox列布局
12.markdown引导 13.image引导
14.frame数目选择框
'''
def read_dropdown_input(choice):
    posepack.vars.flag_button_usbcam = False

    if choice == "usbcam":
        return (
            gr.update(visible=True, interactive=False, value=None), gr.update(visible=True, interactive=True, value="RUN", variant="primary",),
            gr.update(visible=False, interactive=False), 
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(value=None),
            gr.update(visible=True, interactive=True), gr.update(visible=True, interactive=True),
            gr.update(visible=True, interactive=True, value=posepack.vars.flag_flip), gr.update(visible=True, interactive=True, value=posepack.vars.flag_keypoints),
            gr.update(visible=True),
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=True)
        )
    elif choice == "webcam":
        return (
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(visible=True, interactive=True, value=None), 
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(value=None),
            gr.update(visible=True, interactive=True), gr.update(visible=True, interactive=True),
            gr.update(visible=True, interactive=True, value=posepack.vars.flag_flip), gr.update(visible=True, interactive=True, value=posepack.vars.flag_keypoints),
            gr.update(visible=True),
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=True)
        )
    elif choice == "image":
        return (
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(visible=False, interactive=False), 
            gr.update(visible=True, interactive=True, value=None), gr.update(visible=True, interactive=True),
            gr.update(value=None),
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(visible=False, interactive=False, value=posepack.vars.flag_flip), gr.update(visible=True, interactive=True, value=posepack.vars.flag_keypoints),
            gr.update(visible=True),
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=False)
        )
    else:
        return (
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(visible=False, interactive=False), 
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(value=None),
            gr.update(visible=False, interactive=False), gr.update(visible=False, interactive=False),
            gr.update(visible=False, interactive=False, value=posepack.vars.flag_flip), gr.update(visible=False, interactive=False, value=posepack.vars.flag_keypoints),
            gr.update(visible=False),
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=False)
        )

def read_checkbox_flip(value):
    if value:
        posepack.vars.flag_flip = True
        return (
            gr.update(mirror_webcam=True),
            gr.update(mirror_webcam=True)
        )
    else:
        posepack.vars.flag_flip = False
        return (
            gr.update(mirror_webcam=False),
            gr.update(mirror_webcam=False)
        )
    
def read_dropdown_rotate(choice):
    if choice == "90°":
        posepack.vars.rotate = 90
    elif choice == "180°":
        posepack.vars.rotate = 180
    elif choice == "270°":
        posepack.vars.rotate = 270
    else:
        posepack.vars.rotate = 0

def change_button_usbcam():
    posepack.vars.flag_button_usbcam = not posepack.vars.flag_button_usbcam
    if posepack.vars.flag_button_usbcam:
        return gr.update(value="STOP", variant="stop")
    else:
        return gr.update(value="RUN", variant="primary")

def read_dropdown_resolution(choice):
    if choice == "720p":
        posepack.vars.resolution = 720
        return gr.update(webcam_constraints=webcam_constraints_720P)
    elif choice == "540p":
        posepack.vars.resolution = 540
        return gr.update(webcam_constraints=webcam_constraints_540P)
    elif choice == "360p":
        posepack.vars.resolution = 360
        return gr.update(webcam_constraints=webcam_constraints_360P)
    else:
        posepack.vars.resolution = 360
        return gr.update(webcam_constraints=webcam_constraints_360P)

def read_checkbox_keypoints(value):
    if value:
        posepack.vars.flag_keypoints = True
    else:
        posepack.vars.flag_keypoints = False

def read_number_frame(value):
    if value is not None and value >= 1:
        posepack.vars.frame = int(value)
    else:
        posepack.vars.frame = 2

# with gr.Blocks(css="footer {visibility: hidden}") as demo:
with gr.Blocks() as demo:
    gr.Markdown(
        "**<center><font size=6>基于树莓派的人体姿态识别系统</font></center>**"
    )

    with gr.Row(equal_height=True):
        dropdown_input=gr.Dropdown(
            choices=["usbcam", "webcam", "image"],
            value=None,
            allow_custom_value=False,
            filterable=False,
            label="Input",
            interactive=True
        )

        dropdown_model=gr.Dropdown(
            choices=["MediaPipe", "YOLO"],
            value="MediaPipe",
            allow_custom_value=False,
            filterable=False,
            label="Model",
            interactive=True
        )

        dropdown_resolution=gr.Dropdown(
            choices=["360p", "540p", "720p"],
            value="360p",
            allow_custom_value=False,
            filterable=False,
            label="Resolution",
            interactive=True,
            visible=False
        )

        dropdown_rotate=gr.Dropdown(
            choices=["0°", "90°", "180°", "270°"],
            value="0°",
            allow_custom_value=False,
            filterable=False,
            label="Rotate",
            interactive=True,
            visible=False
        )

        number_frame=gr.Number(
            value=2,
            label="Process every N frames",
            interactive=True,
            visible=False,
            minimum=1,
            step=1
        )

        with gr.Column(visible=False) as column_checkbox:
            checkbox_flip=gr.Checkbox(
                value=False,
                label="Flip horizontally",
                interactive=True,
                visible=False
            )

            checkbox_keypoints=gr.Checkbox(
                value=True,
                label="Display Keypoints",
                interactive=True,
                visible=False
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown(
                "**<center><font size=6>Original</font></center>**"
            )
            
            input_guide=gr.Image(
                label="input",
                interactive=False,
                visible=True
            )

            markdown_guide=gr.Markdown(
                value="**<center><font size=5>请从Input中选择一个输入方式</font></center>**",
                visible=True
            )
            
            input_usbcam=gr.Image(
                label="usbcam",
                interactive=False,
                visible=False,
                mirror_webcam=False,
                streaming=True
            )
            
            input_webcam=gr.Image(
                sources="webcam",
                label="webcam",
                interactive=True,
                visible=False,
                mirror_webcam=False,
                streaming=True,
                webcam_constraints=webcam_constraints_360P
            )
            
            input_image=gr.Image(
                sources=["upload", "webcam"],
                label="image",
                interactive=True,
                visible=False
            )

            button_usbcam = gr.Button(
                value="RUN",
                variant="primary",
                interactive=True,
                visible=False
            )
            
            button_image = gr.Button(
                value="RUN",
                variant="primary",
                interactive=True,
                visible=False
            )
        
        with gr.Column():
            gr.Markdown(
                "**<center><font size=6>Processed</font></center>**"
            )

            output_image = gr.Image(
                label="output",
                streaming=True,
                interactive=False,
                mirror_webcam=False
            )
        
        dropdown_input.change(
            read_dropdown_input,
            inputs=dropdown_input,
            outputs=[
                input_usbcam, button_usbcam,
                input_webcam, 
                input_image, button_image,
                output_image,
                dropdown_resolution, dropdown_rotate, checkbox_flip, checkbox_keypoints,
                column_checkbox,
                markdown_guide, input_guide,
                number_frame
            ]
        )

        button_image.click(
            fn=posepack.get_image,
            inputs=input_image,
            outputs=output_image
        )

        input_webcam.stream(
            fn=posepack.get_webcam,
            inputs=input_webcam,
            outputs=[
                input_webcam,
                output_image
            ],
            stream_every=0.05, # 决定webcam输入帧率
            concurrency_limit=30
        )

        checkbox_flip.change(
            fn=read_checkbox_flip,
            inputs=checkbox_flip,
            outputs=[
                input_webcam,
                output_image
            ]
        )

        dropdown_rotate.change(
            fn=read_dropdown_rotate,
            inputs=dropdown_rotate,
            outputs=None
        )

        button_usbcam.click(
            fn=change_button_usbcam,
            inputs=None,
            outputs=button_usbcam
        ).then(
            fn=posepack.get_usbcam,
            inputs=None,
            outputs=[
                input_usbcam,
                output_image
            ]
        )

        dropdown_resolution.change(
            fn=read_dropdown_resolution,
            inputs=dropdown_resolution,
            outputs=input_webcam
        )

        checkbox_keypoints.change(
            fn=read_checkbox_keypoints,
            inputs=checkbox_keypoints,
            outputs=None
        )

        number_frame.change(
            fn=read_number_frame,
            inputs=number_frame,
            outputs=None
        )
