from spotipyio.consts.spotify_consts import TIME_RANGE, LIMIT, SPOTIFY_CURRENT_USER_BASE_URL
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange


class TopItemsCollector(ISpotifyComponent):
    async def run(self, items_type: ItemsType, time_range: TimeRange, limit: int = 50) -> dict:
        url = f"{self._base_url}/{items_type.value}"
        params = {
            TIME_RANGE: time_range.value,
            LIMIT: limit
        }
        return await self._session.get(url=url, params=params)

    @property
    def _base_url(self) -> str:
        return f"{SPOTIFY_CURRENT_USER_BASE_URL}/top"
