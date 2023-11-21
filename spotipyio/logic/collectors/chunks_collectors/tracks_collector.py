from spotipyio.consts.spotify_consts import TRACKS
from spotipyio.contract.collectors.base_chunks_collector import BaseChunksCollector


class TracksCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return TRACKS

    @property
    def _chunk_size(self) -> int:
        return 50
