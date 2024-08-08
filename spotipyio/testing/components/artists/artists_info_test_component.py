from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent


class ArtistsInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return "/artists"

    @property
    def _chunk_size(self) -> int:
        return 50
