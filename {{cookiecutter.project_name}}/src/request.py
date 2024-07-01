from django.http import HttpRequest
from rest_framework.request import Request

from src.models.account.user import User


class HTTPAuthRequest(HttpRequest):
    user: User


class AuthRequest(Request):
    user: User
