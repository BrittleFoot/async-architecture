import os

import requests
from rest_framework import authentication, exceptions
from users.models import User


class OAuth2Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth:
            return None

        token_type, _, token = auth.partition(" ")
        if token_type.lower() != "bearer":
            raise exceptions.AuthenticationFailed("Bearer token not provided")

        is_valid, user_data = self.validate_token(token)
        if not is_valid:
            raise exceptions.AuthenticationFailed("Invalid token")

        user = self.get_user(user_data)

        return (user, token)  # Authentication successful

    def validate_token(self, token):
        introspection_url = os.getenv("AUTH_VALIDATE_TOKEN_HOST")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        response = requests.post(
            introspection_url, data={"token": token}, auth=(client_id, client_secret)
        )

        user_data = response.json()

        if response.status_code != 200 or not user_data.get("active", False):
            return False, {}

        # UNCOMMENT IF YOU WANT PROBLEMS
        # if user_data.get("client_id") != client_id:
        #     raise exceptions.AuthenticationFailed("Invalid client")

        return True, user_data

    def get_user(self, user_data):
        return User.objects.get(public_id=user_data["public_id"])
