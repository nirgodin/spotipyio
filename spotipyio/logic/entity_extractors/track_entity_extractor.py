from typing import Optional

from spotipyio.consts.spotify_consts import NAME
from spotipyio.contract import IEntityExtractor


class TrackEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        return entity.get(NAME)

    @property
    def name(self) -> str:
        return "track"
