from django.urls import path

from apps.accounts.views import LoginView, RegisterView

app_name = "accounts"


def _with_optional_trailing_slash(route: str, view, *, name: str | None = None) -> list:
    normalized = route.rstrip("/")
    return [
        path(f"{normalized}/", view, name=name),
        path(normalized, view),
    ]


urlpatterns = [
    *_with_optional_trailing_slash("register", RegisterView.as_view(), name="register"),
    *_with_optional_trailing_slash("login", LoginView.as_view(), name="login"),
]
