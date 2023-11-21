from spotipyio.contract.collectors.base_chunks_collector import BaseChunksCollector


class AlbumsCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return "albums"

    @property
    def _chunk_size(self) -> int:
        return 20
