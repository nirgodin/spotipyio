from typing import Optional, Dict, Any

from aiohttp import ClientSession

from spotipyio.consts.api_consts import ACCESS_TOKEN
from spotipyio.consts.typing_consts import Json
from spotipyio.logic.authentication.access_token_generator import AccessTokenGenerator
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from spotipyio.utils.web_utils import create_client_session


class SpotifySession:
    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 redirect_uri: Optional[str] = None,
                 grant_type: SpotifyGrantType = SpotifyGrantType.CLIENT_CREDENTIALS,
                 access_code: Optional[str] = None,
                 session: Optional[ClientSession] = None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._grant_type = grant_type
        self._access_code = access_code
        self._session = session

    async def get(self, url: str, params: Optional[dict] = None) -> Json:
        async with self._session.get(url=url, params=params) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def post(self, url: str, payload: dict) -> Json:
        async with self._session.post(url=url, json=payload) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def put(self, url: str, data: Optional[Any] = None, payload: Optional[dict] = None) -> Json:
        async with self._session.put(url=url, data=data, json=payload) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def delete(self, url: str, payload: Optional[dict] = None) -> Json:
        async with self._session.delete(url=url, json=payload) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def __aenter__(self) -> "SpotifySession":
        async with AccessTokenGenerator(self._client_id, self._client_secret, self._redirect_uri) as token_generator:
            response = await token_generator.generate(self._grant_type, self._access_code)

        access_token = response[ACCESS_TOKEN]
        headers = self._build_spotify_headers(access_token)
        raw_session = create_client_session(headers)
        self._session = await raw_session.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    @staticmethod
    def _build_spotify_headers(access_token: str) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
