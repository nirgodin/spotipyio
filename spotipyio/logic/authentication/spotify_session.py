from typing import Optional, Dict

from aiohttp import ClientSession

from spotipyio.consts.api_consts import ACCESS_TOKEN
from spotipyio.consts.typing_consts import Json
from spotipyio.logic.authentication.access_token_generator import AccessTokenGenerator
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType


class SpotifySession:
    def __init__(self, session: Optional[ClientSession] = None):
        self._session = session

    async def get(self, url: str, params: Optional[dict] = None) -> Json:
        async with self._session.get(url=url, params=params) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def post(self, url: str, payload: dict) -> Json:
        async with self._session.post(url=url, json=payload) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def __aenter__(self, grant_type: SpotifyGrantType, access_code: Optional[str] = None) -> "SpotifySession":
        async with AccessTokenGenerator() as token_generator:
            response = await token_generator.generate(grant_type, access_code)

        access_token = response[ACCESS_TOKEN]
        headers = self._build_spotify_headers(access_token)
        session = ClientSession(headers=headers)

        return SpotifySession(session)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.close()

    @staticmethod
    def _build_spotify_headers(access_token: str) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

