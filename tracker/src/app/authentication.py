import os
from datetime import datetime, timedelta, timezone
from hashlib import sha256

import requests
from rest_framework import authentication, exceptions
from users.models import User, UserTokenState


def get_hash(token: str):
    return sha256(token.encode()).hexdigest()


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

    def active_cached_user_token(self, token):
        given_hash = get_hash(token)
        user_token = (
            UserTokenState.objects.prefetch_related("user")
            .filter(token_hash=given_hash, is_active=True)
            .first()
        )
        if not user_token:
            return None

        if user_token.expire_at < datetime.now(timezone.utc):
            user_token.is_active = False
            user_token.save()
            return None

        return {
            "public_id": user_token.user.public_id,
            "username": user_token.user.username,
        }

    def cache_user_token(self, user_data, token):
        user = self.get_user(user_data)
        # trusted_expire = datetime.fromtimestamp(user_data["exp"], timezone.utc)
        pessimistic_expire = datetime.now(timezone.utc) + timedelta(minutes=5)

        UserTokenState.objects.create(
            user=user, token_hash=get_hash(token), expire_at=pessimistic_expire
        )

    def validate_token(self, token):
        if user_data := self.active_cached_user_token(token):
            return True, user_data

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
        self.cache_user_token(user_data, token)

        return True, user_data

    def get_user(self, user_data):
        return User.objects.get(public_id=user_data["public_id"])
