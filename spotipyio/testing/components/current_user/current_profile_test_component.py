from typing import List

from pytest_httpserver import RequestHandler

from spotipyio.testing.infra import BaseTestComponent


class CurrentProfileTestComponent(BaseTestComponent):
    def expect(self) -> List[RequestHandler]:
        request_handler = self._expect_get_request(
            route=f"/me",
        )
        return [request_handler]
