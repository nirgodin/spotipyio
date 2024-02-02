from spotipyio.consts.spotify_consts import TRACKS
from spotipyio.contract import BaseChunksCollector


class TracksCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return TRACKS

    @property
    def _chunk_size(self) -> int:
        return 50
