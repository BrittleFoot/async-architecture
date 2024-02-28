import json

from django.http import JsonResponse
from oauth2_provider import views as oauth2_views
from oauth2_provider.models import get_access_token_model


class IntrospectWithUserInfoTokenView(oauth2_views.IntrospectTokenView):
    def customize(self, token_response: JsonResponse):
        if token_response.status_code != 200:
            return token_response

        token_value = self.request.POST.get("token", self.request.GET.get("token", None))

        token = (
            get_access_token_model().objects.select_related("user").get(token=token_value)
        )

        data = json.loads(token_response.content.decode("utf-8"))
        data["public_id"] = token.user.public_id if token.user else None

        return JsonResponse(data)

    def get(self, request, *args, **kwargs):
        """
        Get the token from the URL parameters.
        URL: https://example.com/introspect?token=mF_9.B5f-4.1JqM

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.customize(super().get(request, *args, **kwargs))

    def post(self, request, *args, **kwargs):
        """
        Get the token from the body form parameters.
        Body: token=mF_9.B5f-4.1JqM

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.customize(super().post(request, *args, **kwargs))
