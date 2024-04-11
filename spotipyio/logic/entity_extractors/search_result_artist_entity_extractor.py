from typing import Optional

from spotipyio.consts.spotify_consts import NAME, ARTISTS, ITEMS
from spotipyio.contract import IEntityExtractor
from spotipyio.utils import safe_nested_get


class SearchResultArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        items = safe_nested_get(entity, [ARTISTS, ITEMS], default=[])

        if items:
            first_item = items[0]
            return first_item[NAME]

    @property
    def name(self) -> str:
        return "artist"
