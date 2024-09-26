from typing import List, Dict

from spotipyio import SpotifyClient
from spotipyio.consts.spotify_consts import CHAPTERS
from spotipyio.consts.typing_consts import Json
from spotipyio.models import ChunkSize
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.managers.base_chunks_collector_test import BaseChunksCollectorTest


class TestChaptersInfo(BaseChunksCollectorTest):
    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.CHAPTERS

    @property
    def _json_response_key(self) -> str:
        return CHAPTERS

    @staticmethod
    def _a_json_response(ids: List[str]) -> Dict[str, List[Json]]:
        return SpotifyMockFactory.several_chapters(ids)

    @staticmethod
    async def _run(ids: List[str], spotify_client: SpotifyClient) -> List[Json]:
        return await spotify_client.chapters.info.run(ids)

    @staticmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        test_client.chapters.info.expect_failure(ids)

    @staticmethod
    def _given_all_responses_successful(ids: List[str], responses: List[Json], test_client: SpotifyTestClient) -> None:
        test_client.chapters.info.expect_success(ids, responses)
