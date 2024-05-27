import sys
from pathlib import Path

from env import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = Env.bool("DEBUG", False)
TEST = (
    "test" in sys.argv
    or sys.argv[0].endswith("pytest")
    or Env.bool("TEST", False)
)

NO_CACHE = Env.bool("NO_CACHE", False)

REDIS_HOST = Env.str("REDIS_HOST")
REDIS_PORT = Env.str("REDIS_PORT")

ENABLE_HEALTH_CHECK = Env.bool("ENABLE_HEALTH_CHECK", False)
ENABLE_SILK_PROFILING = Env.bool("ENABLE_SILK_PROFILING", False)
ENABLE_CPROFILE = Env.bool("ENABLE_CPROFILE", False)
ENABLE_PYINSTRUMENT = Env.bool("ENABLE_PYINSTRUMENT", False)
