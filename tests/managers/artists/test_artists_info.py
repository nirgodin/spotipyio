from random import randint
from typing import List

from _pytest.fixtures import fixture

from spotipyio import SpotifyClient
from spotipyio.consts.typing_consts import Json
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.utils import chain_iterable


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
                                                                     artists_ids: List[List[str]],
                                                                     responses: List[Json],
                                                                     expected: List[dict],
                                                                     test_client: SpotifyTestClient,
                                                                     spotify_client: SpotifyClient):
        provided_ids = chain_iterable(artists_ids)
        self._given_all_responses_successful(
            ids=provided_ids,
            responses=responses,
            test_client=test_client
        )

        actual = await spotify_client.artists.info.run(provided_ids)

        assert actual == expected

    async def test_run__some_responses_unsuccessful__returns_only_successful(
        self,
        artists_ids: List[List[str]],
        responses: List[Json],
        expected: List[dict],
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient
    ):
        successful_ids = chain_iterable(artists_ids)
        unsuccessful_ids = SpotifyMockFactory.some_spotify_ids(randint(1, 200))
        provided_ids = successful_ids + unsuccessful_ids
        self._given_all_responses_successful(
            ids=successful_ids,
            responses=responses,
            test_client=test_client
        )
        self._given_all_responses_unsuccessful(unsuccessful_ids, test_client)

        actual = await spotify_client.artists.info.run(provided_ids)

        assert actual == expected

    @fixture
    def chunks_number(self) -> int:
        return randint(1, 5)

    @fixture
    def artists_ids(self, chunks_number: int) -> List[List[str]]:
        ids = []

        for _ in range(chunks_number):
            chunk_ids = SpotifyMockFactory.some_spotify_ids(50)
            ids.append(chunk_ids)

        return ids

    @fixture
    def responses(self, artists_ids: List[List[str]]) -> List[Json]:
        json_responses = []

        for chunk in artists_ids:
            chunk_responses = SpotifyMockFactory.several_artists(chunk)
            json_responses.append(chunk_responses)

        return json_responses

    @fixture
    def expected(self, responses: List[Json]) -> List[dict]:
        artists = []

        for response in responses:
            response_artists = response["artists"]
            artists.extend(response_artists)

        return artists

    @staticmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        test_client.artists.info.expect_failure(ids)

    @staticmethod
    def _given_all_responses_successful(ids: List[str], responses: List[Json], test_client: SpotifyTestClient) -> None:
        test_client.artists.info.expect_success(ids, responses)
