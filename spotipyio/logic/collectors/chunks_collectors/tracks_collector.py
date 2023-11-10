from aiohttp import ClientSession

from spotipyio.consts.spotify_consts import TRACKS
from spotipyio.contract.collectors.base_chunks_collector import BaseChunksCollector


class TracksCollector(BaseChunksCollector):
    def __init__(self, session: ClientSession):
        super().__init__(session)

    @property
    def _route(self) -> str:
        return TRACKS

    @property
    def _chunk_size(self) -> int:
        return 50
