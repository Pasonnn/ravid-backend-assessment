from __future__ import annotations

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers import LoginSerializer, RegistrationSerializer
from apps.accounts.services import (
    DuplicateEmailError,
    authenticate_user_by_email,
    create_user_account,
    issue_tokens_for_user,
)


def extract_error_message(detail) -> str:
    if isinstance(detail, dict):
        for value in detail.values():
            return extract_error_message(value)
    if isinstance(detail, list):
        if not detail:
            return "Invalid request."
        return extract_error_message(detail[0])
    return str(detail)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": extract_error_message(serializer.errors)}, status=400
            )

        try:
            user = create_user_account(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
        except DuplicateEmailError:
            return Response(
                {"error": "A user with this email already exists."},
                status=400,
            )

        return Response(
            {
                "message": "Registration successful",
                "user_id": user.pk,
            },
            status=200,
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": extract_error_message(serializer.errors)}, status=400
            )

        user = authenticate_user_by_email(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response({"error": "Invalid email or password."}, status=400)

        tokens = issue_tokens_for_user(user)
        return Response(
            {
                "message": "Login successful",
                "access": tokens.access,
                "refresh": tokens.refresh,
            },
            status=200,
        )
