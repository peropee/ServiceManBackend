from .base import *

DEBUG = False
ROOT_URLCONF = "config.urls"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])