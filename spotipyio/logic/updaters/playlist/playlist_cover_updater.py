from typing import Dict

from spotipyio.consts.spotify_consts import IMAGES
from spotipyio.contract import BasePlaylistsUpdater
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools import ImageCompressor


class PlaylistCoverUpdater(BasePlaylistsUpdater):
    def __init__(self,
                 session: SpotifySession,
                 image_compressor: ImageCompressor = ImageCompressor()):
        super().__init__(session)
        self._image_compressor = image_compressor

    async def run(self, playlist_id: str, image: bytes) -> Dict[str, str]:
        url = self._build_url(playlist_id)
        data = self._image_compressor.compress(image)

        return await self._session.put(url=url, data=data)

    @property
    def _route(self) -> str:
        return IMAGES
