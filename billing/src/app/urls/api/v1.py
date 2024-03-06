from django.urls import include, path

urlpatterns = [
    path("v1/tasks/", include("tracker.urls")),
    path("v1/users/", include("users.urls")),
]
