from abc import ABC, abstractmethod
from typing import List

from aiohttp import ClientSession

from spotipyio.consts.spotify_consts import IDS, SPOTIFY_API_BASE_URL
from spotipyio.contract.collectors.base_collector import BaseCollector
from spotipyio.tools.data_chunks_generator import DataChunksGenerator
from spotipyio.utils.general_utils import chain_iterable


class BaseChunksCollector(BaseCollector, ABC):
    def __init__(self, session: ClientSession):
        super().__init__(session)
        self._chunks_generator = DataChunksGenerator(self._chunk_size)
        self._formatted_route = self._route.replace("-", "_")

    async def collect(self, ids: List[str]) -> List[dict]:
        results = await self._chunks_generator.execute_by_chunk_in_parallel(
            lst=ids,
            filtering_list=[],
            func=self._collect_single
        )
        return chain_iterable(results)

    async def _collect_single(self, ids: List[str]) -> List[dict]:
        response = await self._get(url=self._url, params={IDS: ','.join(ids)})
        return response[self._formatted_route]

    @property
    @abstractmethod
    def _chunk_size(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def _route(self) -> str:
        raise NotImplementedError

    @property
    def _url(self) -> str:
        return f"{SPOTIFY_API_BASE_URL}/{self._route}"
