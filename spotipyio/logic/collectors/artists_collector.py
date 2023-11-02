from typing import List, Optional

from aiohttp import ClientSession
from consts.api_consts import ARTISTS_URL_FORMAT
from consts.data_consts import TRACK, ARTISTS, ID
from tools.data_chunks_generator import DataChunksGenerator
from tools.logging import logger

from spotipyio.contract.base_collector import BaseCollector
from spotipyio.utils.general_utils import chain_iterable

MAX_ARTISTS_PER_REQUEST = 50


class ArtistsCollector(BaseCollector):
    def __init__(self, session: ClientSession, chunks_generator: DataChunksGenerator = DataChunksGenerator()):
        super().__init__(session)
        self._chunks_generator = chunks_generator

    async def collect(self, ids: List[str]) -> List[dict]:
        artists = await self._chunks_generator.execute_by_chunk_in_parallel(
            lst=ids,
            filtering_list=[],
            func=self._collect_single
        )
        return chain_iterable(artists)

    async def _collect_single(self, chunk: List[str]) -> List[dict]:  # TODO: Think how to generalize to base class
        response = await self._get(params={"ids": ','.join(chunk)})
        return response[ARTISTS]

    @property
    def _route(self) -> str:
        return "artists"
