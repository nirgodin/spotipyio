from typing import Optional

from spotipyio.consts.spotify_consts import NAME, ARTISTS, ITEMS
from spotipyio.contract import IEntityExtractor
from spotipyio.utils import safe_nested_get


class ArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        items = safe_nested_get(entity, [ARTISTS, ITEMS], default=[])

        if items:
            first_result = items[0]
            return first_result.get(NAME)

    @property
    def name(self) -> str:
        return "artist"
