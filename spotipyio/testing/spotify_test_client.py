from __future__ import annotations
from typing import Optional

from pytest_httpserver import HTTPServer

from spotipyio.testing.managers import *


class SpotifyTestClient:
    def __init__(self,
                 server: Optional[HTTPServer] = None,
                 current_user_manager: Optional[CurrentUserTestManager] = None):
        self._server = server
        self.current_user = current_user_manager

    def get_base_url(self) -> str:
        return self._server.url_for("").rstrip("/")

    @classmethod
    def create(cls, server: HTTPServer) -> SpotifyTestClient:
        return cls(
            server=server,
            current_user_manager=CurrentUserTestManager.create(server=server)
        )
