from spotipyio.consts.spotify_consts import SPOTIFY_CURRENT_USER_BASE_URL
from spotipyio.contract.collectors.base_collector import BaseCollector


class CurrentProfileCollector(BaseCollector):
    async def collect(self):
        return await self._session.get(url=SPOTIFY_CURRENT_USER_BASE_URL)
