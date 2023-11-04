from aiohttp import ClientSession

from spotipyio.contract.collectors.base_chunks_collector import BaseChunksCollector


class AlbumsCollector(BaseChunksCollector):
    def __init__(self, session: ClientSession):
        super().__init__(session)

    @property
    def _route(self) -> str:
        return "albums"

    @property
    def _chunk_size(self) -> int:
        return 20
