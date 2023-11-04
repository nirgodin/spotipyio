from typing import List

from spotipyio.contract.base_collector import BaseCollector
from spotipyio.tools.pool_executor import PoolExecutor


class PlaylistsCollector(BaseCollector):
    async def collect(self, ids: List[str]) -> List[dict]:
        return await PoolExecutor.run(iterable=ids, func=self.collect_single)

    async def collect_single(self, id_: str) -> dict:
        url = self._route_format.format(id=id_)
        return await self._get(url)

    @property
    def _route_format(self) -> str:
        return "playlists/{id}"
