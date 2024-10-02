import os
from typing import Dict, Optional

from aiohttp import ClientSession

from spotipyio.consts.env_consts import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.authentication.authorization_payload_builder import AuthorizationPayloadBuilder
from spotipyio.utils import create_client_session, encode_bearer_token


class AccessTokenGenerator:
    def __init__(self,
                 token_request_url: str,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 redirect_uri: Optional[str] = None,
                 session: Optional[ClientSession] = None):
        self._token_request_url = token_request_url
        self._client_id = client_id or os.environ[SPOTIPY_CLIENT_ID]
        self._client_secret = client_secret or os.environ[SPOTIPY_CLIENT_SECRET]
        self._redirect_uri = redirect_uri or os.environ[SPOTIPY_REDIRECT_URI]
        self._session = session

    async def generate(self, grant_type: SpotifyGrantType, access_code: Optional[str]) -> Dict[str, str]:
        encoded_header = encode_bearer_token(client_id=self._client_id, client_secret=self._client_secret)
        headers = {'Authorization': f"Basic {encoded_header}"}
        data = AuthorizationPayloadBuilder.build(
            grant_type=grant_type,
            access_code=access_code,
            client_id=self._client_id,
            redirect_uri=self._redirect_uri
        )

        async with self._session.post(url=self._token_request_url, headers=headers, data=data) as raw_response:
            raw_response.raise_for_status()
            return await raw_response.json()

    async def __aenter__(self) -> "AccessTokenGenerator":
        raw_session = create_client_session()
        self._session = await raw_session.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
