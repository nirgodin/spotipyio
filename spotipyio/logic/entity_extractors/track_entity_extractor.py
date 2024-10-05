from typing import Optional

from spotipyio.logic.consts.spotify_consts import NAME
from spotipyio.logic.contract import IEntityExtractor


class TrackEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        return entity.get(NAME)

    @property
    def name(self) -> str:
        return "track"
