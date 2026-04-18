from __future__ import annotations

from urllib.parse import urlencode
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.accounts.services import DuplicateEmailError


class AuthenticationApiTests(TestCase):
    def form_post(self, path: str, payload: dict[str, str], **extra):
        return self.client.generic(
            "POST",
            path,
            urlencode(payload),
            content_type="application/x-www-form-urlencoded",
            **extra,
        )

    def test_register_creates_user_with_normalized_email(self) -> None:
        response = self.form_post(
            "/api/register/",
            {
                "email": "User@Example.COM",
                "password": "Sup3rSecret!",
                "confirm_password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["message"], "Registration successful")
        user = get_user_model().objects.get(pk=payload["user_id"])
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.username, "user@example.com")
        self.assertTrue(user.check_password("Sup3rSecret!"))

    def test_register_stays_public_even_with_invalid_auth_header(self) -> None:
        response = self.form_post(
            "/api/register/",
            {
                "email": "public@example.com",
                "password": "Sup3rSecret!",
                "confirm_password": "Sup3rSecret!",
            },
            HTTP_AUTHORIZATION="Bearer invalid",
        )

        self.assertEqual(response.status_code, 200)

    def test_register_requires_confirm_password(self) -> None:
        response = self.form_post(
            "/api/register/",
            {
                "email": "user@example.com",
                "password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "This field is required."})

    def test_register_rejects_password_mismatch(self) -> None:
        response = self.form_post(
            "/api/register/",
            {
                "email": "user@example.com",
                "password": "Sup3rSecret!",
                "confirm_password": "DifferentSecret!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Passwords do not match."})

    def test_register_rejects_invalid_email(self) -> None:
        response = self.form_post(
            "/api/register/",
            {
                "email": "not-an-email",
                "password": "Sup3rSecret!",
                "confirm_password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Enter a valid email address."})

    def test_register_rejects_duplicate_email_case_insensitively(self) -> None:
        user_model = get_user_model()
        user_model.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="Sup3rSecret!",
        )

        response = self.form_post(
            "/api/register/",
            {
                "email": "Existing@Example.com",
                "password": "Sup3rSecret!",
                "confirm_password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "A user with this email already exists."},
        )

    def test_register_handles_duplicate_email_race_from_service_layer(self) -> None:
        with patch(
            "apps.accounts.views.create_user_account",
            side_effect=DuplicateEmailError,
        ):
            response = self.form_post(
                "/api/register/",
                {
                    "email": "user@example.com",
                    "password": "Sup3rSecret!",
                    "confirm_password": "Sup3rSecret!",
                },
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "A user with this email already exists."},
        )

    def test_login_returns_jwt_pair_for_valid_credentials(self) -> None:
        user = get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )

        response = self.form_post(
            "/api/login/",
            {
                "email": "USER@example.com",
                "password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["message"], "Login successful")
        self.assertEqual(AccessToken(payload["access"])["user_id"], str(user.pk))
        self.assertEqual(RefreshToken(payload["refresh"])["user_id"], str(user.pk))

    def test_login_stays_public_even_with_invalid_auth_header(self) -> None:
        get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )

        response = self.form_post(
            "/api/login/",
            {
                "email": "user@example.com",
                "password": "Sup3rSecret!",
            },
            HTTP_AUTHORIZATION="Bearer invalid",
        )

        self.assertEqual(response.status_code, 200)

    def test_login_rejects_unknown_email(self) -> None:
        response = self.form_post(
            "/api/login/",
            {
                "email": "missing@example.com",
                "password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid email or password."})

    def test_login_rejects_wrong_password(self) -> None:
        get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )

        response = self.form_post(
            "/api/login/",
            {
                "email": "user@example.com",
                "password": "WrongPassword!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid email or password."})

    def test_login_requires_email(self) -> None:
        response = self.form_post(
            "/api/login/",
            {
                "password": "Sup3rSecret!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "This field is required."})
