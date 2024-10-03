from random import randint
from typing import List, Optional

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError
from math import ceil

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from tests.testing_utils import an_optional


class TestPlaylistsItemsAdder:
    async def test_run__valid_request__returns_expected_number_of_snapshots(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        playlist_id: str,
        uris: List[str],
        position: Optional[int],
    ):
        test_client.playlists.add_items.expect_success(playlist_id=playlist_id, uris=uris, position=position)
        expected_snapshots_number = ceil(len(uris) / 100)

        actual = await spotify_client.playlists.add_items.run(playlist_id=playlist_id, uris=uris, position=position)

        assert len(actual) == expected_snapshots_number

    async def test_run__any_chunk_fails__raises_client_response_error(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        playlist_id: str,
        uris: List[str],
        position: Optional[int],
    ):
        test_client.playlists.add_items.expect_failure(playlist_id=playlist_id, uris=uris, position=position)

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.add_items.run(playlist_id=playlist_id, uris=uris, position=position)

    @fixture
    def position(self) -> Optional[int]:
        return an_optional(lambda: randint(1, 20))
