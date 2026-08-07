{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
"""RFC 9457 contract checks for the generated API error envelope."""

from __future__ import annotations

from urllib.parse import urlparse


def assert_rfc9457_problem(response: object) -> None:
    status_code = response.status_code
    content_type = response["Content-Type"]
    problem = response.json()

    assert content_type.startswith("application/problem+json")
    assert {"type", "title", "status", "detail", "instance"} <= problem.keys()
    assert problem["status"] == status_code
    assert problem["instance"] == "/api/v1/auth/register"
    assert problem["title"]
    assert problem["detail"]
    assert urlparse(problem["type"]).scheme in {"http", "https"}


def test_api_validation_errors_follow_rfc_9457(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        data="{}",
        content_type="application/json",
    )

    assert response.status_code == 422
    assert_rfc9457_problem(response)
{% endif -%}
