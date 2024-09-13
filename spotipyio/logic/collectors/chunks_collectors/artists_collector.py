from spotipyio.consts.spotify_consts import ARTISTS
from spotipyio.contract import BaseChunksCollector


class ArtistsCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return ARTISTS

    @property
    def _chunk_size(self) -> int:
        return 50
