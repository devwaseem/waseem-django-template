from env import Env
from storages.backends.s3boto3 import S3Boto3Storage

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = True
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "media"
AWS_ACCESS_KEY_ID = Env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = Env.str("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = Env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_REGION_NAME = Env.str("AWS_S3_REGION_NAME")
AWS_S3_HOST = f"{AWS_S3_REGION_NAME}.amazonaws.com"


class StaticStorage(S3Boto3Storage):  # type: ignore
    location = "static"
    default_acl = None


class PublicMediaStorage(S3Boto3Storage):  # type: ignore
    location = "media"
    default_acl = None
    file_overwrite = False


class DBBackupStorage(S3Boto3Storage):  # type: ignore
    location = "db-backups"
    default_acl = None
    file_overwrite = False
