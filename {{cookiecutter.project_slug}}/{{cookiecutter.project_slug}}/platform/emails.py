"""MRML-backed application email rendering and delivery."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import mrml
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def render_mjml_email(template_name: str, context: Mapping[str, Any]) -> str:
    """Render a product-owned MJML template into HTML."""
    mjml = render_to_string(template_name, context)
    rendered_email = mrml.to_html(mjml)
    return rendered_email.content


def send_mjml_email(
    *,
    subject: str,
    recipients: Sequence[str],
    template_name: str,
    context: Mapping[str, Any],
    from_email: str | None = None,
) -> int:
    """Send a multipart email from MRML HTML and an accessible text fallback."""
    html_body = render_mjml_email(template_name, context)
    message = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(html_body),
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=list(recipients),
    )
    message.attach_alternative(html_body, "text/html")
    return message.send()
