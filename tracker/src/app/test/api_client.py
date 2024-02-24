from django.utils.functional import cached_property
from rest_framework.test import APIClient


class AppTestClient:
    @cached_property
    def api_client(self) -> APIClient:
        return APIClient()

    def get(
        self, path: str, expected_status=200, data=None, follow=False, **extra
    ) -> dict:
        result = self.api_client.get(path, data=data, follow=follow, **extra)

        assert result.status_code == expected_status
        return result.json()
