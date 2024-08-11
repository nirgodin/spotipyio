from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class CurrentProfileTestComponent(BaseTestComponent):
    def expect(self) -> List[RequestHandler]:
        request_handler = self._expect_get_request(
            route=f"/me",
        )
        return [request_handler]

    def expect_success(self, response_json: Optional[Json] = None) -> None:
        handler = self._expect_get_request(route=f"/me")
        handler.respond_with_json(
            response_json=response_json or SpotifyMockFactory.user_profile()
        )

    def expect_failure(self, status: Optional[int] = None, response_json: Optional[Json] = None) -> None:
        status, response_json = self._create_invalid_response(status, response_json)
        handler = self._expect_get_request(route=f"/me")
        handler.respond_with_json(
            status=status,
            response_json=response_json
        )
