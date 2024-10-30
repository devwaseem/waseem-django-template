import sys
from pathlib import Path

from env import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = Env.bool("DEBUG")
TEST = "test" in sys.argv or sys.argv[0].endswith("pytest") or Env.bool("TEST")

DOMAIN_NAME = Env.str("DOMAIN_NAME")

NO_CACHE = Env.bool("NO_CACHE")

REDIS_HOST = Env.str("REDIS_HOST")
REDIS_PORT = Env.str("REDIS_PORT")

ENABLE_HEALTH_CHECK = Env.bool("ENABLE_HEALTH_CHECK")
ENABLE_SILK_PROFILING = Env.bool("ENABLE_SILK_PROFILING")
ENABLE_CPROFILE = Env.bool("ENABLE_CPROFILE")
ENABLE_PYINSTRUMENT = Env.bool("ENABLE_PYINSTRUMENT")
ENABLE_SENTRY = Env.bool("ENABLE_SENTRY")


STATIC_USE_WHITENOISE = Env.bool("STATIC_USE_WHITENOISE")
STATIC_USE_S3 = Env.bool("STATIC_USE_S3")
MEDIA_USE_S3 = Env.bool("MEDIA_USE_S3")
