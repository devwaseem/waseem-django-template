from django.http import HttpRequest
from rest_framework.request import Request

from {{cookiecutter.project_name}}.models.account.user import User

class HTTPAuthRequest(HttpRequest):
    user: User

class AuthRequest(Request):
    user: User
