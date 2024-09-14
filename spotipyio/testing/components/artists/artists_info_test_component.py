from spotipyio.consts.spotify_consts import ARTISTS
from spotipyio.consts.typing_consts import Json
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class ArtistsInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{ARTISTS}"

    @property
    def _chunk_size(self) -> int:
        return 50

    @staticmethod
    def _random_valid_response() -> Json:
        return SpotifyMockFactory.several_artists()
