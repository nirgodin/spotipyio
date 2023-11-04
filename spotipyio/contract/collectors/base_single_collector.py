from abc import abstractmethod, ABC
from typing import List

from aiohttp import ClientSession

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.contract.collectors.base_collector import BaseCollector
from spotipyio.tools.pool_executor import PoolExecutor


class BaseSingleCollector(BaseCollector, ABC):
    def __init__(self, session: ClientSession):
        super().__init__(session)

    async def collect(self, ids: List[str]) -> List[dict]:
        return await PoolExecutor.run(iterable=ids, func=self.collect_single)

    async def collect_single(self, id_: str) -> dict:
        route = self._route_format.format(id=id_)
        url = f"{SPOTIFY_API_BASE_URL}/{route}"

        return await self._get(url)

    @property
    @abstractmethod
    def _route_format(self) -> str:
        raise NotImplementedError
