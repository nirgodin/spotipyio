from abc import abstractmethod, ABC
from random import randint
from typing import List, Dict

from _pytest.fixtures import fixture

from spotipyio import SpotifyClient
from spotipyio.consts.typing_consts import Json
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.utils import chain_iterable


class BaseChunksCollectorTest(ABC):
    async def test_run__no_ids_provided__returns_empty_list(self, spotify_client: SpotifyClient):
        actual = await self._run([], spotify_client)
        assert actual == []

    async def test_run__all_responses_unsuccessful__returns_empty_list(self,
                                                                       test_client: SpotifyTestClient,
                                                                       spotify_client: SpotifyClient):
        ids = SpotifyMockFactory.some_spotify_ids(length=randint(1, 200))
        self._given_all_responses_unsuccessful(ids, test_client)

        actual = await self._run(ids, spotify_client)

        assert actual == []

    async def test_run__all_responses_successful__returns_items_list(self,
                                                                     ids: List[List[str]],
                                                                     responses: List[Json],
                                                                     expected: List[dict],
                                                                     test_client: SpotifyTestClient,
                                                                     spotify_client: SpotifyClient):
        provided_ids = chain_iterable(ids)
        self._given_all_responses_successful(
            ids=provided_ids,
            responses=responses,
            test_client=test_client
        )

        actual = await self._run(provided_ids, spotify_client)

        assert actual == expected

    async def test_run__some_responses_unsuccessful__returns_only_successful(
        self,
        ids: List[List[str]],
        responses: List[Json],
        expected: List[dict],
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient
    ):
        successful_ids = chain_iterable(ids)
        unsuccessful_ids = SpotifyMockFactory.some_spotify_ids(randint(1, 200))
        provided_ids = successful_ids + unsuccessful_ids
        self._given_all_responses_successful(
            ids=successful_ids,
            responses=responses,
            test_client=test_client
        )
        self._given_all_responses_unsuccessful(unsuccessful_ids, test_client)

        actual = await self._run(provided_ids, spotify_client)

        assert actual == expected

    @fixture
    def chunks_number(self) -> int:
        return randint(1, 5)

    @fixture
    def ids(self, chunks_number: int) -> List[List[str]]:
        ids = []

        for _ in range(chunks_number):
            chunk_ids = SpotifyMockFactory.some_spotify_ids(self._chunk_size)
            ids.append(chunk_ids)

        return ids

    @fixture
    def responses(self, ids: List[List[str]]) -> List[Json]:
        json_responses = []

        for chunk in ids:
            chunk_responses = self._a_json_response(chunk)
            json_responses.append(chunk_responses)

        return json_responses

    @fixture
    def expected(self, responses: List[Json]) -> List[dict]:
        items = []

        for response in responses:
            response_items = response[self._json_response_key]
            items.extend(response_items)

        return items

    @property
    @abstractmethod
    def _chunk_size(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def _json_response_key(self) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _a_json_response(ids: List[str]) -> Dict[str, List[Json]]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def _run(ids: List[str], spotify_client: SpotifyClient) -> List[Json]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _given_all_responses_successful(ids: List[str], responses: List[Json], test_client: SpotifyTestClient) -> None:
        raise NotImplementedError
