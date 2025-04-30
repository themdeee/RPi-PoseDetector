from webui import demo

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=22229,

        ssl_keyfile="./auth/private.key",
        ssl_certfile="./auth/signed.cer",
        ssl_keyfile_password="12345678",
        ssl_verify=False,

        inbrowser=False,
        show_api=False,

        # auth=("admin", "password")
    )
