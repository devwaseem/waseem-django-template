from typing import Any, TypedDict

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


class DomainContext(TypedDict):
    domain_name: str
    site_name: str | None
    protocol: str
    base_url: str


def get_site_data(request: HttpRequest) -> DomainContext:
    site = get_current_site(request)
    site_name = site.name
    domain_name = site.domain
    protocol = "https" if request.is_secure() else "http"
    base_url = f"{protocol}://{domain_name}"

    return DomainContext(
        domain_name=domain_name,  # type: ignore
        site_name=site_name,  # type: ignore
        protocol=protocol,
        base_url=base_url,
    )


def allauth_settings(_request: HttpRequest) -> dict[str, Any]:  # type: ignore
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": getattr(
            settings, "ACCOUNT_ALLOW_REGISTRATION", True
        )
    }
