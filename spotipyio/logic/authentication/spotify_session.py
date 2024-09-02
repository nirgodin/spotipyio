from typing import Optional, Dict, Any

from aiohttp import ClientSession, ClientResponse, ContentTypeError, ClientResponseError

from spotipyio.consts.api_consts import ACCESS_TOKEN, REFRESH_TOKEN
from spotipyio.consts.typing_consts import Json
from spotipyio.logic.authentication.session_cache_handler_interface import ISessionCacheHandler
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
                 session: Optional[ClientSession] = None,
                 session_cache_handler: Optional[ISessionCacheHandler] = None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._grant_type = grant_type
        self._access_code = access_code
        self._session = session
        self._cache_handler = session_cache_handler

    async def get(self, url: str, params: Optional[dict] = None) -> Optional[Json]:
        async with self._session.get(url=url, params=params) as response:
            return await self._handle_response(response)

    async def post(self, url: str, payload: dict) -> Optional[Json]:
        async with self._session.post(url=url, json=payload) as response:
            return await self._handle_response(response)

    async def put(self, url: str, data: Optional[Any] = None, payload: Optional[dict] = None) -> Optional[Json]:
        async with self._session.put(url=url, data=data, json=payload) as response:
            return await self._handle_response(response)

    async def delete(self, url: str, payload: Optional[dict] = None) -> Optional[Json]:
        async with self._session.delete(url=url, json=payload) as response:
            return await self._handle_response(response)

    async def refresh(self) -> None:
        if self._session is not None:
            await self._session.close()

        raw_session = await self._build_client_session(use_cache=False)
        self._session = await raw_session.__aenter__()

    async def _handle_response(self, response: ClientResponse) -> Optional[Json]:
        if self._is_2xx_successful(response):
            return await self._jsonify_response_if_possible(response)

        json_error_response = await self._jsonify_response_if_possible(response)
        if json_error_response is None:
            response.raise_for_status()

        raise ClientResponseError(
            request_info=response.request_info,
            history=response.history,
            status=response.status,
            message=f"Spotify request to URL `{response.request_info.url}` with method "
                    f"`{response.request_info.method}` failed with the following JSON message:\n{json_error_response}"
        )

    @staticmethod
    def _is_2xx_successful(response: ClientResponse) -> bool:
        return 200 <= response.status < 300

    @staticmethod
    async def _jsonify_response_if_possible(response: ClientResponse) -> Optional[Json]:
        try:
            return await response.json()

        except ContentTypeError:
            return

    async def __aenter__(self) -> "SpotifySession":
        raw_session = await self._build_client_session(use_cache=True)
        self._session = await raw_session.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session is not None:
            await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def _build_client_session(self, use_cache: bool) -> ClientSession:
        response = await self._fetch_access_token(use_cache)
        access_token = response[ACCESS_TOKEN]
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        return create_client_session(headers)

    async def _fetch_access_token(self, use_cache: bool) -> Dict[str, str]:
        if use_cache and self._cache_handler is not None:
            response = await self._retrieve_access_token_from_cache()

            if response is not None:
                return response

        return await self._fetch_new_access_token()

    async def _retrieve_access_token_from_cache(self) -> Optional[Dict[str, str]]:
        cached_response = self._cache_handler.get()
        if cached_response is None:
            return

        async with AccessTokenGenerator(self._client_id, self._client_secret, self._redirect_uri) as token_generator:
            return await token_generator.generate(
                grant_type=SpotifyGrantType.REFRESH_TOKEN,
                access_code=cached_response[REFRESH_TOKEN]
            )

    async def _fetch_new_access_token(self) -> Dict[str, str]:
        async with AccessTokenGenerator(self._client_id, self._client_secret, self._redirect_uri) as token_generator:
            response = await token_generator.generate(self._grant_type, self._access_code)

        if self._cache_handler is not None:
            self._cache_handler.set(response)

        return response
