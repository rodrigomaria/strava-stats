import time
from urllib.parse import urlencode

import requests
from django.conf import settings


class StravaAuthService:
    def __init__(self):
        self.client_id = settings.STRAVA_CLIENT_ID
        self.client_secret = settings.STRAVA_CLIENT_SECRET
        self.redirect_uri = settings.STRAVA_REDIRECT_URI
        self.auth_url = settings.STRAVA_AUTH_URL
        self.token_url = settings.STRAVA_TOKEN_URL

    def get_authorization_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "activity:read_all",
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> dict:
        response = requests.post(
            self.token_url,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()

    def refresh_token(self, refresh_token: str) -> dict:
        response = requests.post(
            self.token_url,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )
        response.raise_for_status()
        return response.json()

    def is_token_expired(self, expires_at: int) -> bool:
        return time.time() >= expires_at

    def get_valid_token(self, session_data: dict) -> dict | None:
        if not session_data.get("access_token"):
            return None

        if self.is_token_expired(session_data.get("expires_at", 0)):
            refresh_token = session_data.get("refresh_token")
            if not refresh_token:
                return None
            try:
                new_token_data = self.refresh_token(refresh_token)
                return new_token_data
            except requests.RequestException:
                return None

        return session_data
