from webui import demo

if __name__ == "__main__":
    demo.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,

        inbrowser=False,
        show_api=False,

        # auth=("admin", "password")
    )
