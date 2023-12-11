from abc import abstractmethod, ABC
from functools import partial
from typing import List, Optional

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools.pool_executor import PoolExecutor


class BaseSingleCollector(ISpotifyComponent, ABC):
    def __init__(self, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(session)
        self._pool_executor = pool_executor

    async def run(self, ids: List[str], **params) -> List[dict]:  # TODO: Think how to better externalize mandatory params
        func = partial(self.run_single, params=params)
        return await self._pool_executor.run(iterable=ids, func=func, expected_type=dict)

    async def run_single(self, id_: str, params: Optional[dict] = None) -> dict:
        route = self._route_format.format(id=id_)
        url = f"{SPOTIFY_API_BASE_URL}/{route}"

        return await self._session.get(url=url, params=params)

    @property
    @abstractmethod
    def _route_format(self) -> str:
        raise NotImplementedError
