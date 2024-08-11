from random import shuffle
from typing import List

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.testing_utils import random_invalid_response


class TestArtistsTopTracks:
    async def test_run__some_valid_some_invalid_responses__returns_only_valid(
            self,
            test_client: SpotifyTestClient,
            spotify_client: SpotifyClient,
            artists_ids: List[str],
            expected: List[dict]
    ):
        actual = await spotify_client.artists.top_tracks.run(artists_ids)

        assert all(response in expected for response in actual)
        assert all(response in actual for response in expected)

    async def test_run_single__valid_response(self,
                                              test_client: SpotifyTestClient,
                                              spotify_client: SpotifyClient):
        artist_id = SpotifyMockFactory.spotify_id()
        expected = SpotifyMockFactory.several_tracks()
        request_handlers = test_client.artists.top_tracks.expect([artist_id])
        request_handlers[0].respond_with_json(expected)

        actual = await spotify_client.artists.top_tracks.run_single(artist_id)

        assert actual == expected

    async def test_run_single__invalid_response(self,
                                                test_client: SpotifyTestClient,
                                                spotify_client: SpotifyClient):
        artist_id = SpotifyMockFactory.spotify_id()
        expected_status_code, expected_response = random_invalid_response()
        request_handlers = test_client.artists.top_tracks.expect([artist_id])
        request_handlers[0].respond_with_json(response_json=expected_response, status=expected_status_code)

        with pytest.raises(ClientResponseError) as exc_info:
            await spotify_client.artists.top_tracks.run_single(artist_id)

        assert exc_info.value.code == expected_status_code
        assert exc_info.value.message.endswith(str(expected_response))

    @fixture
    def valid_artists_ids(self, test_client: SpotifyTestClient) -> List[str]:
        return SpotifyMockFactory.some_spotify_ids()

    @fixture
    def invalid_artists_ids(self, test_client: SpotifyTestClient) -> List[str]:
        ids = SpotifyMockFactory.some_spotify_ids()

        for artist_id in ids:
            test_client.artists.top_tracks.expect_failure(artist_id)

        return ids

    @fixture
    def artists_ids(self,
                    valid_artists_ids: List[str],
                    invalid_artists_ids: List[str]) -> List[str]:
        ids = valid_artists_ids + invalid_artists_ids
        shuffle(ids)

        return ids

    @fixture
    def expected(self, test_client: SpotifyTestClient, valid_artists_ids: List[str]) -> List[dict]:
        responses = []

        for artist_id in valid_artists_ids:
            response_json = SpotifyMockFactory.several_tracks()
            test_client.artists.top_tracks.expect_success(artist_id, response_json)
            responses.append(response_json)

        return responses
