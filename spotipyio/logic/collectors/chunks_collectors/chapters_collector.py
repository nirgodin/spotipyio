from spotipyio.consts.spotify_consts import ALBUMS, CHAPTERS
from spotipyio.contract import BaseChunksCollector
from spotipyio.models import ChunkSize


class ChaptersCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return CHAPTERS

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.CHAPTERS
