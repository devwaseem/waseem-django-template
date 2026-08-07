"""Explicit public API schemas; Django models are never API contracts."""

from __future__ import annotations

from ninja import Schema


class Problem(Schema):
    """RFC 9457-compatible problem details with a stable machine code."""

    type: str
    title: str
    status: int
    detail: str
    instance: str
    code: str
    request_id: str


class UserResponse(Schema):
    """The deliberately minimal generic user representation."""

    id: str
    email: str


class RegisterRequest(Schema):
    email: str
    password: str


class CredentialsRequest(Schema):
    email: str
    password: str


class RefreshRequest(Schema):
    refresh: str


class TokenPairResponse(Schema):
    access: str
    refresh: str


class PasswordResetRequest(Schema):
    email: str


class PasswordResetConfirmRequest(Schema):
    uid: str
    token: str
    password: str
