from random import randint
from typing import List

from _pytest.fixtures import fixture

from spotipyio import SpotifyClient
from spotipyio.consts.spotify_consts import ALBUMS
from spotipyio.consts.typing_consts import Json
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.utils import chain_iterable


class TestAlbumsInfo:
    async def test_run__no_ids_provided__returns_empty_list(self, spotify_client: SpotifyClient):
        actual = await spotify_client.albums.info.run([])
        assert actual == []

    async def test_run__all_responses_unsuccessful__returns_empty_list(self,
                                                                       test_client: SpotifyTestClient,
                                                                       spotify_client: SpotifyClient):
        ids = SpotifyMockFactory.some_spotify_ids(length=randint(1, 100))
        self._given_all_responses_unsuccessful(ids, test_client)

        actual = await spotify_client.albums.info.run(ids)

        assert actual == []

    async def test_run__all_responses_successful__returns_items_list(self,
                                                                     albums_ids: List[List[str]],
                                                                     responses: List[Json],
                                                                     expected: List[dict],
                                                                     test_client: SpotifyTestClient,
                                                                     spotify_client: SpotifyClient):
        provided_ids = chain_iterable(albums_ids)
        self._given_all_responses_successful(
            ids=provided_ids,
            responses=responses,
            test_client=test_client
        )

        actual = await spotify_client.albums.info.run(provided_ids)

        assert actual == expected

    async def test_run__some_responses_unsuccessful__returns_only_successful(
        self,
        albums_ids: List[List[str]],
        responses: List[Json],
        expected: List[dict],
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient
    ):
        successful_ids = chain_iterable(albums_ids)
        unsuccessful_ids = SpotifyMockFactory.some_spotify_ids(randint(1, 200))
        provided_ids = successful_ids + unsuccessful_ids
        self._given_all_responses_successful(
            ids=successful_ids,
            responses=responses,
            test_client=test_client
        )
        self._given_all_responses_unsuccessful(unsuccessful_ids, test_client)

        actual = await spotify_client.albums.info.run(provided_ids)

        assert actual == expected

    @fixture
    def chunks_number(self) -> int:
        return randint(1, 5)

    @fixture
    def albums_ids(self, chunks_number: int) -> List[List[str]]:
        ids = []

        for _ in range(chunks_number):
            chunk_ids = SpotifyMockFactory.some_spotify_ids(20)
            ids.append(chunk_ids)

        return ids

    @fixture
    def responses(self, albums_ids: List[List[str]]) -> List[Json]:
        json_responses = []

        for chunk in albums_ids:
            chunk_responses = SpotifyMockFactory.several_albums(chunk)
            json_responses.append(chunk_responses)

        return json_responses

    @fixture
    def expected(self, responses: List[Json]) -> List[dict]:
        albums = []

        for response in responses:
            response_albums = response[ALBUMS]
            albums.extend(response_albums)

        return albums

    @staticmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        test_client.albums.info.expect_failure(ids)

    @staticmethod
    def _given_all_responses_successful(ids: List[str], responses: List[Json], test_client: SpotifyTestClient) -> None:
        test_client.albums.info.expect_success(ids, responses)
