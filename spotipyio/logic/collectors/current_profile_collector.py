from spotipyio.consts.spotify_consts import SPOTIFY_CURRENT_USER_BASE_URL
from spotipyio.contract.spotify_component_interface import ISpotifyComponent


class CurrentProfileCollector(ISpotifyComponent):
    async def run(self):
        return await self._session.get(url=SPOTIFY_CURRENT_USER_BASE_URL)
