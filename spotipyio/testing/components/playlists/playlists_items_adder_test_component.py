from typing import List, Optional

from pytest_httpserver import RequestHandler, HTTPServer

from spotipyio.consts.spotify_consts import PLAYLISTS, TRACKS, URIS, POSITION, SNAPSHOT_ID
from spotipyio.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.tools import DataChunksGenerator


class PlaylistItemsAdderTestComponent(BaseTestComponent):
    def __init__(self, server: HTTPServer, chunks_generator: DataChunksGenerator = DataChunksGenerator()):
        super().__init__(server)
        self._chunks_generator = chunks_generator

    def expect(self, playlist_id: str, uris: List[str], position: Optional[int] = None) -> List[RequestHandler]:
        return self._create_request_handlers(
            playlist_id=playlist_id,
            uris=uris,
            position=position
        )

    def expect_success(self,
                       playlist_id: str,
                       uris: List[str],
                       position: Optional[int] = None) -> None:
        request_handlers = self._create_request_handlers(
            playlist_id=playlist_id,
            uris=uris,
            position=position
        )

        for handler in request_handlers:
            response = {SNAPSHOT_ID: SpotifyMockFactory.snapshot_id()}
            handler.respond_with_json(
                response_json=response,
                status=201
            )

    def expect_failure(self,
                       playlist_id: str,
                       uris: List[str],
                       position: Optional[int] = None,
                       response_json: Optional[Json] = None,
                       status: Optional[int] = None) -> None:
        request_handlers = self._create_request_handlers(
            playlist_id=playlist_id,
            uris=uris,
            position=position
        )

        for handler in request_handlers:
            status, response_json = self._create_invalid_response(status=status, response_json=response_json)
            handler.respond_with_json(
                status=status,
                response_json=response_json
            )

    def _create_request_handlers(self,
                                 playlist_id: str,
                                 uris: List[str],
                                 position: Optional[int]) -> List[RequestHandler]:
        handlers = []

        for chunk in self._chunks_generator.generate_data_chunks(lst=uris, chunk_size=100):
            payload = {
                URIS: chunk,
                POSITION: position
            }
            handler = self._expect_post_request(
                route=f"/{PLAYLISTS}/{playlist_id}/{TRACKS}",
                payload=payload
            )
            handlers.append(handler)

        return handlers
