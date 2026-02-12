from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse

from app.account.models import User


@pytest.mark.django_db
def test_password_reset_page_renders(client: Client) -> None:
    """Password reset page renders successfully."""
    url = reverse("account_reset_password")
    response = client.get(url)
    assert response.status_code == 200
    assert "Reset password" in response.content.decode()


@pytest.mark.django_db
def test_password_reset_done_page_renders(client: Client) -> None:
    """Password reset done page renders successfully."""
    url = reverse("account_reset_password_done")
    response = client.get(url)
    assert response.status_code == 200
    assert "Check your email" in response.content.decode()


@pytest.mark.django_db
def test_password_reset_from_key_page_renders_invalid_token(
    client: Client,
) -> None:
    """Password reset from key page renders with invalid token message."""
    url = reverse(
        "account_reset_password_from_key",
        kwargs={"uidb36": "invalid", "key": "token"},
    )
    response = client.get(url)
    assert response.status_code == 200
    assert "reset link is invalid" in response.content.decode()


@pytest.mark.django_db
def test_password_reset_from_key_done_page_renders(client: Client) -> None:
    """Password reset from key done page renders successfully."""
    url = reverse("account_reset_password_from_key_done")
    response = client.get(url)
    assert response.status_code == 200
    assert "Password updated" in response.content.decode()


@pytest.mark.django_db
def test_password_reset_post_redirects_to_done(client: Client) -> None:
    """Password reset POST completes without backend errors."""
    user = User.objects.create_user(
        email="reset@example.com",
        password="strong-password",
    )
    url = reverse("account_reset_password")
    response = client.post(url, data={"email": user.email})
    assert response.status_code == 302
    assert response.url == reverse("account_reset_password_done")
