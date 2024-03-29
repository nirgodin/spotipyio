from spotipyio.contract import BaseChunksCollector


class ArtistsCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return "artists"

    @property
    def _chunk_size(self) -> int:
        return 50
