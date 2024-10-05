from random import shuffle
from typing import List, Dict

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.logic.consts.spotify_consts import HREF
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.testing_utils import assert_sorted_equal


class TestUserPlaylistsCollector:
    async def test_run_single__valid_request__returns_paged_playlists(
        self, spotify_client: SpotifyClient, test_client: SpotifyTestClient, user_id: str, paged_playlist: dict
    ):
        test_client.users.playlists.expect_success(user_id, response_json=paged_playlist)
        actual = await spotify_client.users.playlists.run_single(user_id)
        assert actual == paged_playlist

    async def test_run_single__invalid_request__raises_client_response_error(
        self, spotify_client: SpotifyClient, test_client: SpotifyTestClient, user_id: str
    ):
        test_client.users.playlists.expect_failure(user_id)

        with pytest.raises(ClientResponseError):
            await spotify_client.users.playlists.run_single(user_id)

    async def test_run__all_valid_responses__returns_all(
        self, valid_ids_responses_map: Dict[str, dict], test_client: SpotifyTestClient, spotify_client: SpotifyClient
    ):
        self._given_all_responses_valid(valid_ids_responses_map, test_client)
        expected = list(valid_ids_responses_map.values())
        ids = list(valid_ids_responses_map.keys())
        shuffle(ids)

        actual = await spotify_client.users.playlists.run(ids)

        assert_sorted_equal(actual, expected, sort_by=HREF)

    async def test_run__all_invalid_responses__returns_empty_list(
        self, invalid_user_ids: List[str], test_client: SpotifyTestClient, spotify_client: SpotifyClient
    ):
        self._given_all_responses_invalid(invalid_user_ids, test_client)
        actual = await spotify_client.users.playlists.run(invalid_user_ids)
        assert actual == []

    async def test_run__mixed_responses__returns_only_valid(
        self,
        valid_ids_responses_map: Dict[str, dict],
        invalid_user_ids: List[str],
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
    ):
        self._given_all_responses_valid(valid_ids_responses_map, test_client)
        self._given_all_responses_invalid(invalid_user_ids, test_client)
        expected = list(valid_ids_responses_map.values())
        ids = invalid_user_ids + list(valid_ids_responses_map.keys())
        shuffle(ids)

        actual = await spotify_client.users.playlists.run(ids)

        assert_sorted_equal(actual, expected, sort_by=HREF)

    @fixture
    def invalid_user_ids(self) -> List[str]:
        return SpotifyMockFactory.some_spotify_ids()

    @fixture
    def valid_ids_responses_map(self) -> Dict[str, dict]:
        ids_responses_map = {}

        for user_id in SpotifyMockFactory.some_spotify_ids():
            playlist_response = SpotifyMockFactory.paged_playlists(id=user_id)
            ids_responses_map[user_id] = playlist_response

        return ids_responses_map

    @fixture
    def user_id(self) -> str:
        return SpotifyMockFactory.spotify_id()

    @fixture
    def paged_playlist(self, user_id: str) -> dict:
        return SpotifyMockFactory.paged_playlists(id=user_id)

    @staticmethod
    def _given_all_responses_valid(ids_responses_map: Dict[str, dict], test_client: SpotifyTestClient) -> None:
        for user_id, response_json in ids_responses_map.items():
            test_client.users.playlists.expect_success(user_id=user_id, response_json=response_json)

    @staticmethod
    def _given_all_responses_invalid(ids: List[str], test_client: SpotifyTestClient) -> None:
        for user_id in ids:
            test_client.users.playlists.expect_failure(user_id)
