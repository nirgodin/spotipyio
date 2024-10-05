from typing import List, Dict

from spotipyio import SpotifyClient
from spotipyio.logic.consts.spotify_consts import TRACKS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.testing import SpotifyTestClient, SpotifyMockFactory
from tests.managers.base_chunks_collector_test import BaseChunksCollectorTest


class TestTracksInfo(BaseChunksCollectorTest):
    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.TRACKS

    @property
    def _json_response_key(self) -> str:
        return TRACKS

    @staticmethod
    def _a_json_response(ids: List[str]) -> Dict[str, List[Json]]:
        return SpotifyMockFactory.several_tracks(ids)

    @staticmethod
    async def _run(ids: List[str], spotify_client: SpotifyClient) -> List[Json]:
        return await spotify_client.tracks.info.run(ids)

    @staticmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        test_client.tracks.info.expect_failure(ids)

    @staticmethod
    def _given_all_responses_successful(ids: List[str], responses: List[Json], test_client: SpotifyTestClient) -> None:
        test_client.tracks.info.expect_success(ids, responses)
