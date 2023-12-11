from abc import ABC, abstractmethod
from typing import List

from spotipyio.consts.spotify_consts import IDS, SPOTIFY_API_BASE_URL
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools.data_chunks_generator import DataChunksGenerator
from spotipyio.tools.pool_executor import PoolExecutor
from spotipyio.utils.general_utils import chain_iterable


class BaseChunksCollector(ISpotifyComponent, ABC):
    def __init__(self, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(session)
        self._chunks_generator = DataChunksGenerator(pool_executor, self._chunk_size)
        self._formatted_route = self._route.replace("-", "_")

    async def run(self, ids: List[str]) -> List[dict]:
        chunks = await self._chunks_generator.execute_by_chunk_in_parallel(
            lst=ids,
            filtering_list=[],
            func=self._run_single
        )
        results = chain_iterable(chunks)

        return [result for result in results if isinstance(result, dict)]

    async def _run_single(self, ids: List[str]) -> List[dict]:
        response = await self._session.get(url=self._url, params={IDS: ','.join(ids)})
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
