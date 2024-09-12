from __future__ import annotations
from typing import Optional

from pytest_httpserver import HTTPServer

from spotipyio.testing.managers import *


class SpotifyTestClient:
    def __init__(self,
                 server: Optional[HTTPServer] = None,
                 artists_manager: Optional[ArtistsTestManager] = None,
                 current_user_manager: Optional[CurrentUserTestManager] = None,
                 playlists_manager: Optional[PlaylistsTestManager] = None,
                 users_manager: Optional[UsersTestManager] = None):
        self._server = server
        self.artists = artists_manager
        self.current_user = current_user_manager
        self.playlists = playlists_manager
        self.users = users_manager

    def get_base_url(self) -> str:
        return self._server.url_for("").rstrip("/")

    @classmethod
    def create(cls, server: HTTPServer) -> SpotifyTestClient:
        return cls(
            server=server,
            artists_manager=ArtistsTestManager.create(server),
            current_user_manager=CurrentUserTestManager.create(server),
            playlists_manager=PlaylistsTestManager.create(server),
            users_manager=UsersTestManager.create(server)
        )
