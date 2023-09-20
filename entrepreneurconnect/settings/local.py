from entrepreneurconnect.settings.base import ALLOWED_HOSTS

DEBUG = True

ALLOWED_HOSTS += [
    "http://localhost:3000",
    "localhost",
    "127.0.0.1",
]