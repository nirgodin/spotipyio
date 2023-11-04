from aiohttp import ClientSession

from spotipyio.contract.base_chunks_collector import BaseChunksCollector


class TracksCollector(BaseChunksCollector):
    def __init__(self, session: ClientSession):
        super().__init__(session)

    @property
    def _route(self) -> str:
        return "tracks"

    @property
    def _chunk_size(self) -> int:
        return 50
