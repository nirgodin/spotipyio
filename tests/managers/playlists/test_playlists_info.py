from random import shuffle
from typing import Dict, List

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TestPlaylistsInfo:
    async def test_run_single__valid_response(self, test_client: SpotifyTestClient, spotify_client: SpotifyClient):
        playlist_id = SpotifyMockFactory.spotify_id()
        expected = SpotifyMockFactory.playlist(id=playlist_id)
        test_client.playlists.info.expect_success(
            id_=playlist_id,
            response_json=expected
        )

        actual = await spotify_client.playlists.info.run_single(playlist_id)

        assert actual == expected

    async def test_run_single__invalid_response__raises_client_response_error(self,
                                                                              test_client: SpotifyTestClient,
                                                                              spotify_client: SpotifyClient):
        playlist_id = SpotifyMockFactory.spotify_id()
        test_client.playlists.info.expect_failure(id_=playlist_id)

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.info.run_single(playlist_id)

    async def test_run__valid_response(self,
                                       valid_ids_to_responses_map: Dict[str, dict],
                                       test_client: SpotifyTestClient,
                                       spotify_client: SpotifyClient):
        self._given_all_responses_valid(valid_ids_to_responses_map, test_client)
        expected = list(valid_ids_to_responses_map.values())
        ids = list(valid_ids_to_responses_map.keys())

        actual = await spotify_client.playlists.info.run(ids)

        assert actual == expected

    async def test_run__all_invalid_responses__returns_empty_list(self,
                                                                  invalid_ids: List[str],
                                                                  test_client: SpotifyTestClient,
                                                                  spotify_client: SpotifyClient):
        self._given_all_responses_invalid(invalid_ids, test_client)
        actual = await spotify_client.playlists.info.run(invalid_ids)
        assert actual == []

    async def test_run__mixed_responses__returns_only_valid(self,
                                                            valid_ids_to_responses_map: Dict[str, dict],
                                                            invalid_ids: List[str],
                                                            test_client: SpotifyTestClient,
                                                            spotify_client: SpotifyClient):
        self._given_all_responses_valid(valid_ids_to_responses_map, test_client)
        self._given_all_responses_invalid(invalid_ids, test_client)
        expected = list(valid_ids_to_responses_map.values())
        ids = invalid_ids + list(valid_ids_to_responses_map.keys())
        shuffle(ids)

        actual = await spotify_client.playlists.info.run(ids)

        assert sorted(actual, key=lambda x: x["id"]) == sorted(expected, key=lambda x: x["id"])

    @fixture
    def valid_ids_to_responses_map(self) -> Dict[str, dict]:
        ids_responses_map = {}

        for playlist_id in SpotifyMockFactory.some_spotify_ids():
            playlist_response = SpotifyMockFactory.playlist(id=playlist_id)
            ids_responses_map[playlist_id] = playlist_response

        return ids_responses_map

    @fixture
    def invalid_ids(self) -> List[str]:
        return SpotifyMockFactory.some_spotify_ids()

    @staticmethod
    def _given_all_responses_valid(ids_responses_map: Dict[str, dict], test_client: SpotifyTestClient) -> None:
        for playlist_id, response_json in ids_responses_map.items():
            test_client.playlists.info.expect_success(id_=playlist_id, response_json=response_json)

    @staticmethod
    def _given_all_responses_invalid(ids: List[str], test_client: SpotifyTestClient) -> None:
        for playlist_id in ids:
            test_client.playlists.info.expect_failure(playlist_id)
