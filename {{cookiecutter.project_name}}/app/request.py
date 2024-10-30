from django.http import HttpRequest
from rest_framework.request import Request

from app.models.account.user import User


class HTTPAuthRequest(HttpRequest):
    user: User


class AuthRequest(Request):
    user: User
