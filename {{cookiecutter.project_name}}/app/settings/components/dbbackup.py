from app.settings.vars import DEBUG

DBBACKUP_STORAGE = "app.settings.components.aws.DBBackupStorage"
DBBACKUP_CLEANUP_KEEP = 7

if DEBUG:
    DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
    DBBACKUP_STORAGE_OPTIONS = {"location": "./data"}
