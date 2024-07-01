import sentry_sdk
from env import Env

sentry_dsn = Env.str("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=Env.float("SENTRY_TRACES_SAMPLE_RATE"),
    )
