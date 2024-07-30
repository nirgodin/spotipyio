from typing import List, Optional

from spotipyio.consts.spotify_consts import URIS, TRACKS
from spotipyio.contract import BasePlaylistsUpdater
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools import DataChunksGenerator


class PlaylistItemsAdder(BasePlaylistsUpdater):
    def __init__(self, session: SpotifySession, chunks_generator: DataChunksGenerator = DataChunksGenerator()):
        super().__init__(session)
        self._chunks_generator = chunks_generator

    async def run(self, playlist_id: str, uris: List[str], position: Optional[int] = None) -> None:
        chunks = self._chunks_generator.generate_data_chunks(
            lst=uris,
            chunk_size=self._chunk_size
        )
        url = self._build_url(playlist_id)

        for chunk in chunks:
            payload = {
                URIS: chunk,
                "position": position
            }

            await self._session.post(url=url, payload=payload)

    @property
    def _route(self) -> str:
        return TRACKS

    @property
    def _chunk_size(self) -> int:
        return 100
