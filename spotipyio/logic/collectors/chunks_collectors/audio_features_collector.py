from spotipyio.contract import BaseChunksCollector


class AudioFeaturesCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return "audio-features"

    @property
    def _chunk_size(self) -> int:
        return 100
