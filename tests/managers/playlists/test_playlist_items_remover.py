from math import ceil
from random import randint
from typing import List, Optional, Dict

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.testing_utils import an_optional


class TestPlaylistsItemsRemover:
    async def test_run__valid_request__returns_last_removal_snapshot_id(self,
                                                                        test_client: SpotifyTestClient,
                                                                        spotify_client: SpotifyClient,
                                                                        playlist_id: str,
                                                                        uris: List[str],
                                                                        expected_snapshots: List[str],
                                                                        first_snapshot_id: str):
        test_client.playlists.remove_items.expect_success(
            playlist_id=playlist_id,
            uris=uris,
            snapshot_id=first_snapshot_id,
            expected_snapshots=expected_snapshots
        )

        actual = await spotify_client.playlists.remove_items.run(
            playlist_id=playlist_id,
            uris=uris,
            snapshot_id=first_snapshot_id
        )

        assert actual == expected_snapshots[-1]

    async def test_run__any_chunk_fails__raises_client_response_error(self,
                                                                      test_client: SpotifyTestClient,
                                                                      spotify_client: SpotifyClient,
                                                                      playlist_id: str,
                                                                      uris: List[str],
                                                                      first_snapshot_id: str):
        test_client.playlists.remove_items.expect_failure(
            playlist_id=playlist_id,
            uris=uris,
            snapshot_id=first_snapshot_id
        )

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.remove_items.run(
                playlist_id=playlist_id,
                uris=uris,
                snapshot_id=first_snapshot_id
            )

    @fixture
    def first_snapshot_id(self) -> str:
        return SpotifyMockFactory.snapshot_id()

    @fixture
    def expected_snapshots(self, uris: List[str]) -> List[str]:
        return [SpotifyMockFactory.snapshot_id() for _ in range(0, len(uris), 100)]
