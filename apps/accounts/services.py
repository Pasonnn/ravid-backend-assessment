from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError, transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import normalize_email


@dataclass
class TokenPair:
    access: str
    refresh: str


class DuplicateEmailError(Exception):
    pass


def create_user_account(email: str, password: str):
    user_model = get_user_model()
    normalized_email = normalize_email(email)

    try:
        with transaction.atomic():
            return user_model.objects.create_user(
                username=normalized_email,
                email=normalized_email,
                password=password,
            )
    except IntegrityError as exc:
        raise DuplicateEmailError from exc


def authenticate_user_by_email(email: str, password: str):
    normalized_email = normalize_email(email)
    user_model = get_user_model()
    user = user_model.objects.filter(email__iexact=normalized_email).first()
    if user is None:
        return None

    authenticated_user = authenticate(username=user.username, password=password)
    if authenticated_user is None or not authenticated_user.is_active:
        return None
    return authenticated_user


def issue_tokens_for_user(user) -> TokenPair:
    refresh = RefreshToken.for_user(user)
    return TokenPair(
        access=str(refresh.access_token),
        refresh=str(refresh),
    )
