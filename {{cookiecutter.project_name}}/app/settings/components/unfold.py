from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "{{cookiecutter.project_name}}",
    "SITE_HEADER": "{{cookiecutter.project_name}}",
    "SITE_URL": "/admin",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": True,
        "navigation": [
            {
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:app_user_changelist"),
                    },
                ],
            },
        ],
    },
}
