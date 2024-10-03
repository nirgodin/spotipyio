from __future__ import annotations

from typing import Optional
from urllib.parse import urlencode

from pytest_httpserver import HTTPServer

from spotipyio import SpotifyClient, SpotifySession
from spotipyio.consts.api_consts import ACCESS_TOKEN
from spotipyio.logic.authentication import SpotifyGrantType, AuthorizationPayloadBuilder
from spotipyio.testing.managers import (
    AlbumsTestManager,
    ArtistsTestManager,
    ChaptersTestManager,
    CurrentUserTestManager,
    EpisodesTestManager,
    PlaylistsTestManager,
    SearchTestManager,
    TracksTestManager,
    UsersTestManager,
)
from spotipyio.utils import random_alphanumeric_string


class SpotifyTestClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        grant_type: SpotifyGrantType = SpotifyGrantType.CLIENT_CREDENTIALS,
        access_code: Optional[str] = None,
        api_server: Optional[HTTPServer] = None,
        authorization_server: Optional[HTTPServer] = None,
        session: Optional[SpotifySession] = None,
        albums_manager: Optional[AlbumsTestManager] = None,
        artists_manager: Optional[ArtistsTestManager] = None,
        chapters_manager: Optional[ChaptersTestManager] = None,
        current_user_manager: Optional[CurrentUserTestManager] = None,
        episodes_manager: Optional[EpisodesTestManager] = None,
        playlists_manager: Optional[PlaylistsTestManager] = None,
        search_manager: Optional[SearchTestManager] = None,
        tracks_manager: Optional[TracksTestManager] = None,
        users_manager: Optional[UsersTestManager] = None,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._grant_type = grant_type
        self._access_code = access_code
        self._api_server = api_server
        self._authorization_server = authorization_server
        self._session = session
        self.albums = albums_manager
        self.artists = artists_manager
        self.chapters = chapters_manager
        self.current_user = current_user_manager
        self.episodes = episodes_manager
        self.playlists = playlists_manager
        self.search = search_manager
        self.tracks = tracks_manager
        self.users = users_manager

    def get_base_url(self) -> str:
        return self._api_server.url_for("").rstrip("/")

    def create_client(self) -> SpotifyClient:
        return SpotifyClient.create(session=self._session, base_url=self.get_base_url())

    async def __aenter__(self) -> "SpotifyTestClient":
        self._init_api_server()
        self._init_authorization_server()
        self._expect_authorization_request()
        await self._init_session()
        self._init_managers()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._api_server is not None and self._api_server.is_running():
            self._api_server.stop()

        if self._authorization_server is not None and self._authorization_server.is_running():
            self._authorization_server.stop()

    def _init_api_server(self):
        if self._api_server is None:
            self._api_server = HTTPServer()

        if not self._api_server.is_running():
            self._api_server.start()

    def _init_authorization_server(self):
        if self._authorization_server is None:
            self._authorization_server = HTTPServer()

        if not self._authorization_server.is_running():
            self._authorization_server.start()

    def _expect_authorization_request(self) -> None:
        payload = AuthorizationPayloadBuilder.build(
            grant_type=self._grant_type,
            access_code=self._access_code,
            client_id=self._client_id,
            redirect_uri=self._redirect_uri,
        )
        request_handler = self._authorization_server.expect_request(
            uri="/", method="POST", data=bytes(urlencode(payload).encode())
        )
        authorization_server_response = {ACCESS_TOKEN: random_alphanumeric_string()}
        request_handler.respond_with_json(authorization_server_response)

    async def _init_session(self):
        if self._session is None:
            self._session = SpotifySession(
                token_request_url=self._authorization_server.url_for("").rstrip("/"),
                client_id=self._client_id,
                client_secret=self._client_secret,
                redirect_uri=self._redirect_uri,
                grant_type=self._grant_type,
            )

        self._session = await self._session.__aenter__()

    def _init_managers(self) -> None:
        headers = self._session.get_authorization_headers()
        self.albums = AlbumsTestManager.create(self._api_server, headers)
        self.artists = ArtistsTestManager.create(self._api_server, headers)
        self.chapters = ChaptersTestManager.create(self._api_server, headers)
        self.current_user = CurrentUserTestManager.create(self._api_server, headers)
        self.episodes = EpisodesTestManager.create(self._api_server, headers)
        self.playlists = PlaylistsTestManager.create(self._api_server, headers)
        self.search = SearchTestManager.create(self._api_server, headers)
        self.tracks = TracksTestManager.create(self._api_server, headers)
        self.users = UsersTestManager.create(self._api_server, headers)
