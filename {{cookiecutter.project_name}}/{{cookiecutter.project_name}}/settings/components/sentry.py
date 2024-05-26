import sentry_sdk
from env import Env

sentry_dsn = Env("SENTRY_DSN", str, default=None)  # type: ignore

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=Env("SENTRY_TRACES_SAMPLE_RATE", float, 0),  # type: ignore
    )
