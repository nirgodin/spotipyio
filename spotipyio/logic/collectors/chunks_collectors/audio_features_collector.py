from spotipyio.consts.spotify_consts import AUDIO_FEATURES_ROUTE
from spotipyio.contract import BaseChunksCollector
from spotipyio.models import ChunkSize


class AudioFeaturesCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return AUDIO_FEATURES_ROUTE

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.AUDIO_FEATURES
