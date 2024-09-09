from typing import Optional

from spotipyio.consts.spotify_consts import NAME, ARTISTS, ITEMS
from spotipyio.contract import IEntityExtractor
from spotipyio.utils import safe_nested_get


class PrimaryArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        items = entity.get(ARTISTS)

        if items:
            primary_artist = items[0]
            return primary_artist.get(NAME)

    @property
    def name(self) -> str:
        return "artist"
