from random import randint
from typing import List, Tuple

from _pytest.fixtures import fixture

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.utils import chain_iterable
from tests.testing_utils import random_invalid_response, random_boolean


class TestArtistsInfo:
    async def test_run__no_ids_provided__returns_empty_list(self, spotify_client: SpotifyClient):
        actual = await spotify_client.artists.info.run([])
        assert actual == []

    async def test_run__all_responses_unsuccessful__returns_empty_list(self,
                                                                       test_client: SpotifyTestClient,
                                                                       spotify_client: SpotifyClient):
        ids = SpotifyMockFactory.some_spotify_ids(length=randint(1, 200))
        self._given_all_responses_unsuccessful(ids, test_client)

        actual = await spotify_client.artists.info.run(ids)

        assert actual == []

    async def test_run__all_responses_successful__returns_items_list(self,
                                                                     chunks_responses_map: List[Tuple[List[str], dict]],
                                                                     expected: List[dict],
                                                                     test_client: SpotifyTestClient,
                                                                     spotify_client: SpotifyClient):
        artists_ids = [chunk[0] for chunk in chunks_responses_map]
        provided_ids = chain_iterable(artists_ids)
        self._given_all_responses_successful(chunks_responses_map, test_client)

        actual = await spotify_client.artists.info.run(provided_ids)

        assert actual == expected

    async def test_run__some_responses_unsuccessful__returns_only_successful(
        self,
        chunks_responses_map: List[Tuple[List[str], dict]],
        expected: List[dict],
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient
    ):
        artists_ids = [chunk[0] for chunk in chunks_responses_map]
        successful_ids = chain_iterable(artists_ids)
        unsuccessful_ids = SpotifyMockFactory.some_spotify_ids(randint(1, 200))
        provided_ids = successful_ids + unsuccessful_ids
        self._given_all_responses_successful(chunks_responses_map, test_client)
        self._given_all_responses_unsuccessful(unsuccessful_ids, test_client)

        actual = await spotify_client.artists.info.run(provided_ids)

        assert actual == expected

    @fixture
    def chunks_responses_map(self) -> List[Tuple[List[str], dict]]:
        chunks_map = []

        for _ in range(randint(1, 5)):
            chunk_ids = SpotifyMockFactory.some_spotify_ids(50)
            chunk_response = SpotifyMockFactory.several_artists(chunk_ids)
            chunks_map.append((chunk_ids, chunk_response))

        return chunks_map

    @fixture
    def expected(self, chunks_responses_map: List[Tuple[List[str], dict]]) -> List[dict]:
        artists = []

        for ids, response in chunks_responses_map:
            response_artists = response["artists"]
            artists.extend(response_artists)

        return artists

    @staticmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        request_handlers = test_client.artists.info.expect(ids)

        for handler in request_handlers:
            status, response_json = random_invalid_response()
            handler.respond_with_json(response_json=response_json, status=status)

    @staticmethod
    def _given_all_responses_successful(chunks_responses_map: List[Tuple[List[str], dict]],
                                        test_client: SpotifyTestClient) -> None:
        for ids, response_json in chunks_responses_map:
            request_handlers = test_client.artists.info.expect(ids)
            request_handlers[0].respond_with_json(response_json)
