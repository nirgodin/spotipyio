from random import randint
from typing import List

from _pytest.fixtures import fixture

from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


@fixture
def playlist_id() -> str:
    return SpotifyMockFactory.spotify_id()

@fixture
def uris() -> List[str]:
    length = randint(1, 500)
    return SpotifyMockFactory.some_uris(entity_type="track", length=length)
