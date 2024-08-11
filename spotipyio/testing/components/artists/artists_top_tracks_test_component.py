from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.consts.typing_consts import Json
from spotipyio.testing.infra.base_test_component import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class ArtistsTopTracksTestComponent(BaseTestComponent):
    def expect(self, ids: List[str]) -> List[RequestHandler]:
        request_handlers = []

        for artist_id in ids:
            handler = self._expect_get_request(f"/artists/{artist_id}/top-tracks")
            request_handlers.append(handler)

        return request_handlers

    def expect_success(self, id_: str, response_json: Optional[Json] = None) -> None:
        response = response_json or SpotifyMockFactory.several_tracks()
        self._expect_get_request(f"/artists/{id_}/top-tracks").respond_with_json(response)

    def expect_failure(self, id_: str, status: Optional[int] = None, response_json: Optional[Json] = None) -> None:
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handler = self._expect_get_request(f"/artists/{id_}/top-tracks")
        request_handler.respond_with_json(
            response_json=response_json,
            status=status
        )