from typing import Dict, Optional

from spotipyio.consts.spotify_consts import IMAGES
from spotipyio.contract import BasePlaylistsUpdater
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools import ImageCompressor
from spotipyio.utils import encode_image_to_base64


class PlaylistCoverUpdater(BasePlaylistsUpdater):
    def __init__(self, base_url: str, session: SpotifySession, image_compressor: ImageCompressor = ImageCompressor()):
        super().__init__(base_url=base_url, session=session)
        self._image_compressor = image_compressor

    async def run(self, playlist_id: str, image: bytes, compress_if_needed: bool = True) -> None:
        url = self._build_url(playlist_id)

        if compress_if_needed:
            image = self._image_compressor.compress(image)

        if image is not None:
            data = encode_image_to_base64(image)
            await self._session.put(url=url, data=data)

    @property
    def _route(self) -> str:
        return IMAGES
