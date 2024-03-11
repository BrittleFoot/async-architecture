from django.urls import include, path

urlpatterns = [
    path("v2/tasks/", include("tracker.v2urls")),
]
