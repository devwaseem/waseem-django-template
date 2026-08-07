from __future__ import annotations

from django.core import mail
from django.test import override_settings

from {{ cookiecutter.project_slug }}.platform.emails import (
    render_mjml_email,
    send_mjml_email,
)

TEST_MJML_TEMPLATE = """
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text>Hello {{ '{{' }} recipient_name {{ '}}' }}.</mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
"""
TEST_TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {"email/test.mjml": TEST_MJML_TEMPLATE},
                )
            ],
        },
    }
]


@override_settings(TEMPLATES=TEST_TEMPLATES)
def test_mjml_email_renderer_renders_a_product_template() -> None:
    html = render_mjml_email("email/test.mjml", {"recipient_name": "Avery"})

    assert "<html" in html.lower()
    assert "Hello Avery." in html


@override_settings(TEMPLATES=TEST_TEMPLATES)
def test_mjml_email_sender_adds_an_html_and_text_part() -> None:
    delivered = send_mjml_email(
        subject="Welcome",
        recipients=["avery@example.test"],
        template_name="email/test.mjml",
        context={"recipient_name": "Avery"},
    )

    assert delivered == 1
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.from_email == "no-reply@example.test"
    assert message.to == ["avery@example.test"]
    assert "Hello Avery." in message.body
    assert message.alternatives[0].mimetype == "text/html"
    assert "Hello Avery." in message.alternatives[0].content
