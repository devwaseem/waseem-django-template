REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
        # "rest_framework.permissions.DjangoModelPermissions",
        # "src.permissions.IsAPIKeyAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ["src.auth.APIKeyAuthentication"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_verbose_name }} API",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.IsAdminUser",
    ],
    # OTHER SETTINGS
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}
