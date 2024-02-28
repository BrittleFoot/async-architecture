from django.urls import path
from oauth2_provider import urls
from oauth2_provider import views as oauth2_views

from app.authorization import IntrospectWithUserInfoTokenView

app_name = "oauth2_provider"

urlpatterns = (
    [
        # Base urls
        path("authorize/", oauth2_views.AuthorizationView.as_view(), name="authorize"),
        path("token/", oauth2_views.TokenView.as_view(), name="token"),
        path(
            "revoke_token/",
            oauth2_views.RevokeTokenView.as_view(),
            name="revoke-token",
        ),
        path(
            "introspect/",
            IntrospectWithUserInfoTokenView.as_view(),
            name="introspect",
        ),
    ]
    + urls.management_urlpatterns
    + urls.oidc_urlpatterns
)
