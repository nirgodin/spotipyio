from abc import ABC, abstractmethod
from typing import List

from pytest_httpserver import HTTPServer, RequestHandler

from spotipyio.consts.spotify_consts import IDS
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.tools import DataChunksGenerator


class BaseChunksTestComponent(BaseTestComponent, ABC):
    def __init__(self, server: HTTPServer, chunks_generator: DataChunksGenerator = DataChunksGenerator()):
        super().__init__(server)
        self._chunks_generator = chunks_generator

    def expect(self, ids: List[str]) -> List[RequestHandler]:
        return self._expect_chunks(
            route=self._route,
            ids=ids,
            chunk_size=self._chunk_size
        )

    def _expect_chunks(self, route: str, ids: List[str], chunk_size: int) -> List[RequestHandler]:
        chunks = self._chunks_generator.generate_data_chunks(lst=ids, chunk_size=chunk_size)
        request_handlers = []

        for chunk in chunks:
            chunk_handler = self._expect_get_request(
                route=route,
                params={IDS: ','.join(chunk)}
            )
            request_handlers.append(chunk_handler)

        return request_handlers

    @property
    @abstractmethod
    def _chunk_size(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def _route(self) -> str:
        raise NotImplementedError
