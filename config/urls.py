from django.urls import include, path

urlpatterns = [
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.files.urls")),
    path("api/", include("apps.operations.urls")),
]
