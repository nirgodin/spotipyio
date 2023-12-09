from abc import abstractmethod, ABC
from typing import List, Optional

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools.pool_executor import PoolExecutor


class BaseSingleCollector(ISpotifyComponent, ABC):
    def __init__(self, pool_executor: PoolExecutor = PoolExecutor(), session: Optional[SpotifySession] = None):
        super().__init__(session)
        self._pool_executor = pool_executor

    async def run(self, ids: List[str]) -> List[dict]:
        return await self._pool_executor.run(iterable=ids, func=self.collect_single, expected_type=dict)

    async def collect_single(self, id_: str) -> dict:
        route = self._route_format.format(id=id_)
        url = f"{SPOTIFY_API_BASE_URL}/{route}"

        return await self._session.get(url)

    @property
    @abstractmethod
    def _route_format(self) -> str:
        raise NotImplementedError
