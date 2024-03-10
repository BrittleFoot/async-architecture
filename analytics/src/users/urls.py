from django.urls import path

from users.api.views import UsersMeView

urlpatterns = [
    path("me/", UsersMeView.as_view(), name="me"),
]
