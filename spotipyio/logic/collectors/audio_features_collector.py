from aiohttp import ClientSession

from spotipyio.contract.base_chunks_collector import BaseChunksCollector


class AudioFeaturesCollector(BaseChunksCollector):
    def __init__(self, session: ClientSession):
        super().__init__(session)

    @property
    def _route(self) -> str:
        return "audio-features"

    @property
    def _chunk_size(self) -> int:
        return 100
