from spotipyio.consts.spotify_consts import CHAPTERS
from spotipyio.consts.typing_consts import Json
from spotipyio.models import ChunkSize
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class ChaptersInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{CHAPTERS}"

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.CHAPTERS

    @staticmethod
    def _random_valid_response() -> Json:
        return SpotifyMockFactory.several_chapters()