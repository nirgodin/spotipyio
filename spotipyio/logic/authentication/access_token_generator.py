import base64
import os
from typing import Dict, Optional

from aiohttp import ClientSession

from spotipyio.consts.api_consts import TOKEN_REQUEST_URL, REDIRECT_URI, CODE, GRANT_TYPE, JSON, REFRESH_TOKEN, \
    CLIENT_ID
from spotipyio.consts.env_consts import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI

from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from spotipyio.utils.web_utils import create_client_session


class AccessTokenGenerator:
    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 redirect_uri: Optional[str] = None,
                 session: Optional[ClientSession] = None):
        self._client_id = client_id or os.environ[SPOTIPY_CLIENT_ID]
        self._client_secret = client_secret or os.environ[SPOTIPY_CLIENT_SECRET]
        self._redirect_uri = redirect_uri or os.environ[SPOTIPY_REDIRECT_URI]
        self._session = session

    async def generate(self, grant_type: SpotifyGrantType, access_code: Optional[str]) -> Dict[str, str]:
        encoded_header = self._get_encoded_header()
        headers = {'Authorization': f"Basic {encoded_header}"}
        data = self._build_request_payload(access_code, grant_type)

        async with self._session.post(url=TOKEN_REQUEST_URL, headers=headers, data=data) as raw_response:
            raw_response.raise_for_status()
            return await raw_response.json()

    def _get_encoded_header(self) -> str:
        bytes_auth = bytes(f"{self._client_id}:{self._client_secret}", "ISO-8859-1")
        b64_auth = base64.b64encode(bytes_auth)

        return b64_auth.decode('ascii')

    def _build_request_payload(self, access_code: str, grant_type: SpotifyGrantType) -> dict:
        if grant_type == SpotifyGrantType.AUTHORIZATION_CODE:
            return {
                GRANT_TYPE: grant_type.value,
                CODE: access_code,
                REDIRECT_URI: self._redirect_uri,
                JSON: True
            }

        elif grant_type == SpotifyGrantType.REFRESH_TOKEN:
            return {
                GRANT_TYPE: grant_type.value,
                REFRESH_TOKEN: access_code,
                CLIENT_ID: self._client_id
            }

        elif grant_type == SpotifyGrantType.CLIENT_CREDENTIALS:
            return {
                GRANT_TYPE: grant_type.value,
                JSON: True
            }

        else:
            raise ValueError('Did not recognize grant type')

    async def __aenter__(self) -> "AccessTokenGenerator":
        raw_session = create_client_session()
        self._session = await raw_session.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
