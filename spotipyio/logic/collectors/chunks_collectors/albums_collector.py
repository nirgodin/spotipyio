from spotipyio.consts.spotify_consts import ALBUMS
from spotipyio.contract import BaseChunksCollector


class AlbumsCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return ALBUMS

    @property
    def _chunk_size(self) -> int:
        return 20
