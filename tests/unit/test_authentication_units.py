from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase, SimpleTestCase
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.accounts.serializers import LoginSerializer, RegistrationSerializer
from apps.accounts.services import (
    DuplicateEmailError,
    TokenPair,
    authenticate_user_by_email,
    create_user_account,
    issue_tokens_for_user,
    normalize_email,
)
from apps.accounts.views import LoginView, RegisterView, extract_error_message


class AuthenticationUtilityTests(SimpleTestCase):
    def test_normalize_email_strips_and_lowercases(self) -> None:
        self.assertEqual(normalize_email("  User@Example.COM "), "user@example.com")

    def test_extract_error_message_flattens_nested_serializer_errors(self) -> None:
        error = {"email": ["This field is required."]}
        self.assertEqual(extract_error_message(error), "This field is required.")

    def test_extract_error_message_handles_empty_lists(self) -> None:
        self.assertEqual(extract_error_message([]), "Invalid request.")

    def test_auth_views_override_default_permissions_and_authentication(self) -> None:
        self.assertEqual(RegisterView.permission_classes, [AllowAny])
        self.assertEqual(LoginView.permission_classes, [AllowAny])
        self.assertEqual(RegisterView.authentication_classes, [])
        self.assertEqual(LoginView.authentication_classes, [])


class AuthenticationSerializerTests(TestCase):
    def test_registration_serializer_rejects_duplicate_email(self) -> None:
        get_user_model().objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="Sup3rSecret!",
        )
        serializer = RegistrationSerializer(
            data={
                "email": "Existing@Example.com",
                "password": "Sup3rSecret!",
                "confirm_password": "Sup3rSecret!",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["email"][0],
            "A user with this email already exists.",
        )

    def test_registration_serializer_rejects_password_mismatch(self) -> None:
        serializer = RegistrationSerializer(
            data={
                "email": "user@example.com",
                "password": "Sup3rSecret!",
                "confirm_password": "DifferentSecret!",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0], "Passwords do not match."
        )

    def test_login_serializer_normalizes_email(self) -> None:
        serializer = LoginSerializer(
            data={
                "email": "User@Example.com",
                "password": "Sup3rSecret!",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["email"], "user@example.com")


class AuthenticationServiceTests(TestCase):
    def test_create_user_account_sets_username_to_normalized_email(self) -> None:
        user = create_user_account("User@Example.com", "Sup3rSecret!")

        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.username, "user@example.com")
        self.assertTrue(user.check_password("Sup3rSecret!"))

    def test_create_user_account_raises_duplicate_email_error_for_existing_user(
        self,
    ) -> None:
        create_user_account("user@example.com", "Sup3rSecret!")

        with self.assertRaises(DuplicateEmailError):
            create_user_account("USER@example.com", "AnotherSecret!")

    def test_authenticate_user_by_email_returns_user_for_valid_credentials(
        self,
    ) -> None:
        user = get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )

        authenticated_user = authenticate_user_by_email(
            "User@Example.com",
            "Sup3rSecret!",
        )

        self.assertEqual(authenticated_user, user)

    def test_authenticate_user_by_email_returns_none_for_wrong_password(self) -> None:
        get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )

        self.assertIsNone(
            authenticate_user_by_email("user@example.com", "WrongPassword!")
        )

    def test_authenticate_user_by_email_returns_none_for_unknown_email(self) -> None:
        self.assertIsNone(
            authenticate_user_by_email("missing@example.com", "Sup3rSecret!")
        )

    def test_authenticate_user_by_email_returns_none_for_inactive_user(self) -> None:
        user = get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )
        user.is_active = False
        user.save(update_fields=["is_active"])

        self.assertIsNone(
            authenticate_user_by_email("user@example.com", "Sup3rSecret!")
        )

    def test_issue_tokens_for_user_returns_parseable_jwt_pair(self) -> None:
        user = get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="Sup3rSecret!",
        )

        tokens = issue_tokens_for_user(user)

        self.assertIsInstance(tokens, TokenPair)
        self.assertEqual(AccessToken(tokens.access)["user_id"], str(user.pk))
        self.assertEqual(RefreshToken(tokens.refresh)["user_id"], str(user.pk))
