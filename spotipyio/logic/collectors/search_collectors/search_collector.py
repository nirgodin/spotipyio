from typing import List, Optional

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.tools import PoolExecutor


class SearchCollector(ISpotifyComponent):
    def __init__(self, pool_executor: PoolExecutor = PoolExecutor(), session: Optional[SpotifySession] = None):
        super().__init__(session)
        self._pool_executor = pool_executor

    async def run(self, search_items: List[SearchItem]):
        return await self._pool_executor.run(iterable=search_items, func=self.run_single, expected_type=dict)

    async def run_single(self, search_item: SearchItem) -> dict:
        return await self._session.get(url=self._url, params=search_item.to_query_params())

    @property
    def _route(self) -> str:
        return "search"

    @property
    def _url(self) -> str:
        return f"{SPOTIFY_API_BASE_URL}/{self._route}"
