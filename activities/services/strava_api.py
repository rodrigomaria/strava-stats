import requests
from django.conf import settings

from ..constants import EPOCH_TIMESTAMP, QUANTITY_PER_PAGE


class StravaAPIService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = settings.STRAVA_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_athlete(self) -> dict:
        response = requests.get(f"{self.base_url}/athlete", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_all_activities(self, after_timestamp: float = None) -> list:
        if after_timestamp is None:
            after_timestamp = EPOCH_TIMESTAMP

        all_activities = []
        page = 1

        while True:
            response = requests.get(
                f"{self.base_url}/athlete/activities",
                headers=self.headers,
                params={
                    "after": after_timestamp,
                    "page": page,
                    "per_page": QUANTITY_PER_PAGE,
                },
            )

            if response.status_code != 200:
                break

            activities = response.json()
            if not activities:
                break

            all_activities.extend(activities)
            page += 1

        return all_activities
