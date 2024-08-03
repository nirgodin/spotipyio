from pytest_httpserver import RequestHandler

from spotipyio.testing.infra import BaseTestComponent


class CurrentProfileTestComponent(BaseTestComponent):
    def expect(self) -> RequestHandler:
        return self._expect_get_request(
            route=f"/me",
        )
