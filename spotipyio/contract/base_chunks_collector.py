from abc import ABC, abstractmethod
from typing import List

from aiohttp import ClientSession

from spotipyio.consts.spotify_consts import IDS
from spotipyio.contract.base_collector import BaseCollector
from spotipyio.tools.data_chunks_generator import DataChunksGenerator
from spotipyio.utils.general_utils import chain_iterable


class BaseChunksCollector(ABC, BaseCollector):
    def __init__(self, session: ClientSession):
        super().__init__(session)
        self._chunks_generator = DataChunksGenerator(self._chunk_size)
        self._formatted_route = self._route.replace("-", "-")

    async def collect(self, ids: List[str]) -> List[dict]:
        artists = await self._chunks_generator.execute_by_chunk_in_parallel(
            lst=ids,
            filtering_list=[],
            func=self._collect_single
        )
        return chain_iterable(artists)

    async def _collect_single(self, chunk: List[str]) -> List[dict]:
        response = await self._get(params={IDS: ','.join(chunk)})
        return response[self._formatted_route]

    @abstractmethod
    @property
    def _chunk_size(self) -> int:
        raise NotImplementedError
