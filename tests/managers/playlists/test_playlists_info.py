from copy import deepcopy
from random import shuffle, randint
from typing import Dict, List
from urllib.parse import urlencode

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.consts.spotify_consts import ID, TRACKS, ITEMS, PLAYLISTS, OFFSET, LIMIT
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.managers.conftest import base_url
from tests.testing_utils import assert_sorted_equal


class TestPlaylistsInfo:
    async def test_run_single__single_page__valid_response(self,
                                                           test_client: SpotifyTestClient,
                                                           spotify_client: SpotifyClient,
                                                           playlist_id: str):
        expected = SpotifyMockFactory.playlist(id=playlist_id)
        test_client.playlists.info.expect_success(
            id_=playlist_id,
            response_jsons=[expected]
        )

        actual = await spotify_client.playlists.info.run_single(playlist_id)

        assert actual == expected

    async def test_run_single__multiple_pages_all_requested__returns_all_pages_items(self,
                                                                                     base_url: str,
                                                                                     test_client: SpotifyTestClient,
                                                                                     spotify_client: SpotifyClient,
                                                                                     playlist_id: str,
                                                                                     max_pages: int):
        response_jsons = self._random_paged_response_jsons(
            base_url=base_url,
            playlist_id=playlist_id,
            max_pages=max_pages
        )
        expected = self._build_expected_paged_response(response_jsons, requested_pages=max_pages)
        test_client.playlists.info.expect_success(
            id_=playlist_id,
            response_jsons=response_jsons,
            expected_pages=max_pages
        )

        actual = await spotify_client.playlists.info.run_single(playlist_id, max_pages=max_pages)

        assert actual == expected

    async def test_run_single__multiple_pages_requested_less_than_existing__returns_only_requested_pages_items(
            self,
            base_url: str,
            test_client: SpotifyTestClient,
            spotify_client: SpotifyClient,
            playlist_id: str,
            max_pages: int
    ):
        requested_pages = max_pages - 1
        response_jsons = self._random_paged_response_jsons(
            base_url=base_url,
            playlist_id=playlist_id,
            max_pages=max_pages
        )
        expected = self._build_expected_paged_response(response_jsons, requested_pages=requested_pages)
        test_client.playlists.info.expect_success(
            id_=playlist_id,
            response_jsons=response_jsons,
            expected_pages=max_pages
        )

        actual = await spotify_client.playlists.info.run_single(playlist_id, max_pages=requested_pages)

        assert actual == expected

    async def test_run_single__invalid_response__raises_client_response_error(self,
                                                                              test_client: SpotifyTestClient,
                                                                              spotify_client: SpotifyClient,
                                                                              playlist_id: str):
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

        assert_sorted_equal(actual, expected, sort_by=ID)

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

    @fixture
    def max_pages(self) -> int:
        return randint(2, 5)

    def _random_paged_response_jsons(self,
                                     base_url: str,
                                     playlist_id: str,
                                     max_pages: int) -> List[dict]:
        tracks = SpotifyMockFactory.playlist_tracks(next=self._build_next_url(base_url, playlist_id, page_number=1))
        playlist_response = SpotifyMockFactory.playlist(id=playlist_id, tracks=tracks, total=100)
        additional_pages_responses = self._build_additional_pages_responses(
            max_pages=max_pages,
            base_url=base_url,
            playlist_id=playlist_id
        )

        return [playlist_response] + additional_pages_responses

    def _build_additional_pages_responses(self, max_pages: int, base_url: str, playlist_id: str) -> List[dict]:
        additional_pages_responses = []

        for i in range(1, max_pages):
            next_url = self._build_next_url(base_url, playlist_id, page_number=i + 1)
            page_response = SpotifyMockFactory.playlist_tracks(id=playlist_id, next=next_url)
            additional_pages_responses.append(page_response)

        return additional_pages_responses

    @staticmethod
    def _build_next_url(base_url: str, playlist_id: str, page_number: int) -> str:
        params = {
            OFFSET: str(page_number * 100),
            LIMIT: "100"
        }
        encoded_params = urlencode(params)

        return f"{base_url}/{PLAYLISTS}/{playlist_id}/{TRACKS}?{encoded_params}"

    @staticmethod
    def _build_expected_paged_response(response_jsons: List[dict], requested_pages: int) -> dict:
        response = deepcopy(response_jsons[0])

        for i in range(1, requested_pages):
            page_response = response_jsons[i]
            page_items = page_response[ITEMS]
            response[TRACKS][ITEMS].extend(page_items)

        return response

    @staticmethod
    def _given_all_responses_valid(ids_responses_map: Dict[str, dict], test_client: SpotifyTestClient) -> None:
        for playlist_id, response_json in ids_responses_map.items():
            test_client.playlists.info.expect_success(id_=playlist_id, response_jsons=[response_json])

    @staticmethod
    def _given_all_responses_invalid(ids: List[str], test_client: SpotifyTestClient) -> None:
        for playlist_id in ids:
            test_client.playlists.info.expect_failure(playlist_id)
