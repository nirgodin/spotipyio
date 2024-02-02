from typing import Optional

from spotipyio.consts.spotify_consts import NAME, ARTISTS
from spotipyio.contract import IEntityExtractor


class ArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        artists = entity.get(ARTISTS)

        if artists:
            main_artist = artists[0]
            return main_artist.get(NAME)

    @property
    def name(self) -> str:
        return "artist"
