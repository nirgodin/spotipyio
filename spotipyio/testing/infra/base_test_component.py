from abc import ABC, abstractmethod
from typing import Optional, List
from urllib.parse import urlencode

from pytest_httpserver import HTTPServer
from pytest_httpserver.httpserver import HandlerType, RequestHandler


class BaseTestComponent(ABC):
    def __init__(self, server: HTTPServer):
        self._server = server

    @abstractmethod
    def expect(self, *args, **kwargs) -> List[RequestHandler]:
        raise NotImplementedError

    def _expect_get_request(self, route: str, params: Optional[dict] = None, encode: bool = False) -> RequestHandler:
        if params is not None and encode:
            params = urlencode(params)

        return self._server.expect_request(
            uri=route,
            query_string=params,
            method="GET",
            handler_type=HandlerType.ONESHOT
        )

    def _expect_post_request(self, route: str, payload: dict) -> RequestHandler:
        return self._server.expect_request(
            uri=route,
            method="POST",
            json=payload,
            handler_type=HandlerType.ONESHOT
        )
