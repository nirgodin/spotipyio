from spotipyio.logic.consts.spotify_consts import EPISODES
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.models import ChunkSize
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class EpisodesInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{EPISODES}"

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.EPISODES

    @staticmethod
    def _random_valid_response() -> Json:
        return SpotifyMockFactory.several_episodes()
