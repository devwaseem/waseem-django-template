"""Storage defaults: private signed media and public static assets."""

from storages.backends.s3 import S3Storage


class PrivateMediaStorage(S3Storage):
    """Keep uploads private and issue signed URLs by default."""

    location = "media"
    default_acl = "private"
    querystring_auth = True


class PublicStaticStorage(S3Storage):
    """Serve static assets publicly via an S3 bucket policy or CDN."""

    location = "static"
    default_acl = None
    querystring_auth = False
