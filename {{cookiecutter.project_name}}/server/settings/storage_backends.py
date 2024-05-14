from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):  # type: ignore
    location = "static"
    default_acl = "public-read"


class PublicMediaStorage(S3Boto3Storage):  # type: ignore
    location = "media"
    default_acl = "public-read"
    file_overwrite = False


class DBBackupStorage(S3Boto3Storage):  # type: ignore
    location = "db-backups"
    default_acl = "private"
    file_overwrite = False
