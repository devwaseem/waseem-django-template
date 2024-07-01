from env import Env

# MJML: https://github.com/liminspace/django-mjml#tcpserver-mode
MJML_BACKEND_MODE = "tcpserver"
MJML_TCPSERVERS = [
    (Env("MJML_HOST"), Env("MJML_PORT")),
]
