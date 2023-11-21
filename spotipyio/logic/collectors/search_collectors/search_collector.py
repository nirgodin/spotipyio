from typing import List

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.contract.collectors.base_collector import BaseCollector
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.tools.pool_executor import PoolExecutor


class SearchCollector(BaseCollector):
    async def collect(self, search_items: List[SearchItem]):
        return await PoolExecutor.run(iterable=search_items, func=self.collect_single)

    async def collect_single(self, search_item: SearchItem) -> dict:
        return await self._session.get(url=self._url, params=search_item.to_query_params())

    @property
    def _route(self) -> str:
        return "search"

    @property
    def _url(self) -> str:
        return f"{SPOTIFY_API_BASE_URL}/{self._route}"
