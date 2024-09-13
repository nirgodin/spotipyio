from typing import List

from spotipyio.consts.spotify_consts import ALBUMS
from spotipyio.consts.typing_consts import Json
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class AlbumsInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{ALBUMS}"

    @property
    def _chunk_size(self) -> int:
        return 20

    def _random_valid_responses(self, handlers_number: int) -> List[Json]:
        return [SpotifyMockFactory.several_albums() for _ in range(handlers_number)]
