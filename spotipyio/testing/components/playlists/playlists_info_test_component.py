from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.consts.spotify_consts import PLAYLISTS
from spotipyio.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class PlaylistsInfoTestComponent(BaseTestComponent):
    def expect(self, id_: str, max_pages: int = 1) -> List[RequestHandler]:
        return [self._create_request_handler(id_)]

    def expect_success(self, id_: str, response_json: Optional[Json] = None, max_pages: int = 1) -> None:
        self._validate_max_pages(max_pages)
        request_handler = self._create_request_handler(id_)
        response = response_json or SpotifyMockFactory.playlist(id=id_)

        request_handler.respond_with_json(response)

    def expect_failure(self,
                       id_: str,
                       status: Optional[int] = None,
                       response_json: Optional[Json] = None,
                       max_pages: int = 1) -> None:
        self._validate_max_pages(max_pages)
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handler = self._create_request_handler(id_)

        request_handler.respond_with_json(
            status=status,
            response_json=response_json
        )

    @staticmethod
    def _validate_max_pages(max_pages: int) -> None:
        if max_pages > 1:
            raise ValueError("Only max_pages=1 is supported at the moment")

    def _create_request_handler(self, id_: str) -> RequestHandler:
        return self._server.expect_request(f"/{PLAYLISTS}/{id_}")
