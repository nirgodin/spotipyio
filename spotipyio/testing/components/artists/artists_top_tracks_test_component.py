from typing import List

from pytest_httpserver import RequestHandler

from spotipyio.testing.infra.base_test_component import BaseTestComponent


class ArtistsTopTracksTestComponent(BaseTestComponent):
    def expect(self, ids: List[str]) -> List[RequestHandler]:
        request_handlers = []

        for artist_id in ids:
            handler = self._expect_get_request(f"/artists/{artist_id}/top-tracks")
            request_handlers.append(handler)

        return request_handlers
