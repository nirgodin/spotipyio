from spotipyio.consts.spotify_consts import TRACKS
from spotipyio.consts.typing_consts import Json
from spotipyio.models import ChunkSize
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TracksInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{TRACKS}"

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.TRACKS

    @staticmethod
    def _random_valid_response() -> Json:
        return SpotifyMockFactory.several_tracks()
