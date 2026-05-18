from typing import Any

import httpx

from app.core.config import settings


class ArtInstituteClient:
    def __init__(self):
        self.base_url = settings.ART_API_URL
        self._cache: dict[str, dict[str, Any]] = {}

    async def get_artwork(self, external_id: str) -> dict[str, Any] | None:
        if external_id in self._cache:
            return self._cache[external_id]

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/artworks/{external_id}")
            if response.status_code == 200:
                data = response.json()
                self._cache[external_id] = data
                return data
            return None


art_client = ArtInstituteClient()
