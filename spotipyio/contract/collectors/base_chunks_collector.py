from abc import ABC, abstractmethod
from typing import List

from spotipyio.consts.spotify_consts import IDS
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools import DataChunksGenerator
from spotipyio.utils.general_utils import chain_iterable


class BaseChunksCollector(ISpotifyComponent, ABC):
    def __init__(self, base_url: str, session: SpotifySession, chunks_generator: DataChunksGenerator = DataChunksGenerator()):
        super().__init__(base_url=base_url, session=session)
        self._chunks_generator = chunks_generator
        self._formatted_route = self._route.replace("-", "_")

    async def run(self, ids: List[str]) -> List[dict]:
        chunks = await self._chunks_generator.execute_by_chunk_in_parallel(
            lst=ids,
            func=self._run_single,
            expected_type=list,
            chunk_size=self._chunk_size
        )
        return chain_iterable(chunks)

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
        return f"{self._base_url}/{self._route}"
