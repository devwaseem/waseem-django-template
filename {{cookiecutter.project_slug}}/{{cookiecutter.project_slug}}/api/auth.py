"""Generic email/password JWT endpoints with refresh rotation and revocation."""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ninja import Router
from ninja.errors import HttpError
from ninja.security import HttpBearer
from ninja_jwt.exceptions import TokenError
from ninja_jwt.tokens import AccessToken, RefreshToken

from {{ cookiecutter.project_slug }}.api.schemas import (
    CredentialsRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    Problem,
    RefreshRequest,
    RegisterRequest,
    TokenPairResponse,
    UserResponse,
)


def problem(
    request: HttpRequest,
    *,
    status: int,
    code: str,
    title: str,
    detail: str,
) -> JsonResponse:
    """Return an RFC 9457 problem response without exposing internals."""
    body = Problem(
        type=f"https://httpstatuses.com/{status}",
        title=title,
        status=status,
        detail=detail,
        instance=request.path,
        code=code,
        request_id=getattr(request, "request_id", ""),
    ).model_dump()
    return JsonResponse(body, status=status, content_type="application/problem+json")


def serialize_user(user: Any) -> UserResponse:
    """Map the model to a stable public contract explicitly."""
    return UserResponse(id=str(user.pk), email=user.email)


def token_pair_for(user: Any) -> TokenPairResponse:
    """Create an access and refresh token for one active user."""
    refresh = RefreshToken.for_user(user)
    return TokenPairResponse(access=str(refresh.access_token), refresh=str(refresh))


class JwtBearer(HttpBearer):
    """Database-backed bearer authentication for protected API routes."""

    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        try:
            access = AccessToken(token)
            user_id = access["user_id"]
            return get_user_model().objects.filter(pk=user_id, is_active=True).first()
        except KeyError, TokenError:
            return None


router = Router(tags=["Authentication"])
bearer_auth = JwtBearer()


@router.post("/register", response={201: UserResponse, 403: Problem, 409: Problem})
def register(
    request: HttpRequest, payload: RegisterRequest
) -> UserResponse | JsonResponse:
    """Register a generic account when registration is enabled by environment."""
    if not settings.ACCOUNT_ALLOW_REGISTRATION:
        return problem(
            request,
            status=403,
            code="registration_disabled",
            title="Registration is disabled",
            detail="This service is not accepting new accounts.",
        )
    email = get_user_model().objects.normalize_email(payload.email).lower()
    if get_user_model().objects.filter(email__iexact=email).exists():
        return problem(
            request,
            status=409,
            code="email_already_registered",
            title="Account already exists",
            detail="An account with this email address already exists.",
        )
    try:
        password_validation.validate_password(payload.password)
    except ValidationError as error:
        raise HttpError(422, "; ".join(error.messages)) from error
    user = get_user_model().objects.create_user(email=email, password=payload.password)
    return 201, serialize_user(user)


@router.post("/token", response={200: TokenPairResponse, 401: Problem})
def obtain_token(
    request: HttpRequest,
    payload: CredentialsRequest,
) -> TokenPairResponse | JsonResponse:
    """Exchange valid email/password credentials for a fresh token pair."""
    user = authenticate(request, email=payload.email, password=payload.password)
    if user is None:
        return problem(
            request,
            status=401,
            code="invalid_credentials",
            title="Authentication failed",
            detail="The email or password is incorrect.",
        )
    return token_pair_for(user)


@router.post("/token/refresh", response={200: TokenPairResponse, 401: Problem})
def refresh_token(
    request: HttpRequest,
    payload: RefreshRequest,
) -> TokenPairResponse | JsonResponse:
    """Rotate a valid refresh token and blacklist the token it replaces."""
    try:
        previous_refresh = RefreshToken(payload.refresh)
        user = get_user_model().objects.get(
            pk=previous_refresh["user_id"], is_active=True
        )
        previous_refresh.blacklist()
    except get_user_model().DoesNotExist, KeyError, TokenError:
        return problem(
            request,
            status=401,
            code="invalid_refresh_token",
            title="Refresh failed",
            detail="The refresh token is invalid or has expired.",
        )
    return token_pair_for(user)


@router.post("/token/revoke", response={204: None, 401: Problem})
def revoke_token(
    request: HttpRequest, payload: RefreshRequest
) -> HttpResponse | JsonResponse:
    """Blacklist the supplied refresh token to end its session."""
    try:
        RefreshToken(payload.refresh).blacklist()
    except TokenError:
        return problem(
            request,
            status=401,
            code="invalid_refresh_token",
            title="Revoke failed",
            detail="The refresh token is invalid or has expired.",
        )
    return HttpResponse(status=204)


@router.get("/me", auth=bearer_auth, response={200: UserResponse})
def current_user(request: HttpRequest) -> UserResponse:
    """Return the authenticated user's minimal public representation."""
    return serialize_user(request.auth)


@router.post("/password/reset", response={202: None})
def request_password_reset(
    request: HttpRequest,
    payload: PasswordResetRequest,
) -> HttpResponse:
    """Send a reset email when an active user exists, without enumeration."""
    user = (
        get_user_model()
        .objects.filter(email__iexact=payload.email, is_active=True)
        .first()
    )
    if user is not None:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_path = "/api/v1/auth/password/reset/confirm"
        reset_url = request.build_absolute_uri(f"{reset_path}?uid={uid}&token={token}")
        send_mail(
            subject="Reset your password",
            message=f"Use this link to reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    return HttpResponse(status=202)


@router.post("/password/reset/confirm", response={204: None, 400: Problem})
def confirm_password_reset(
    request: HttpRequest,
    payload: PasswordResetConfirmRequest,
) -> HttpResponse | JsonResponse:
    """Set a new password for a valid, unexpired reset token."""
    try:
        user_id = force_str(urlsafe_base64_decode(payload.uid))
        user = get_user_model().objects.get(pk=user_id, is_active=True)
    except ValueError, get_user_model().DoesNotExist:
        user = None
    if user is None or not default_token_generator.check_token(user, payload.token):
        return problem(
            request,
            status=400,
            code="invalid_reset_token",
            title="Reset failed",
            detail="The reset link is invalid or has expired.",
        )
    try:
        password_validation.validate_password(payload.password, user=user)
    except ValidationError as error:
        raise HttpError(422, "; ".join(error.messages)) from error
    user.set_password(payload.password)
    user.save(update_fields=["password"])
    return HttpResponse(status=204)
