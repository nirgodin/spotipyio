from typing import Optional

from spotipyio.consts.spotify_consts import NAME, ARTISTS
from spotipyio.contract import IEntityExtractor


class TrackSearchResultArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> Optional[str]:
        artists = entity.get(ARTISTS)

        if artists:
            first_artist = artists[0]
            return first_artist.get(NAME)

    @property
    def name(self) -> str:
        return "artist"
