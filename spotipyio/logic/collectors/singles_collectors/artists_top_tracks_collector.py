from spotipyio.contract import BaseSingleCollector


class ArtistsTopTracksCollector(BaseSingleCollector):
    @property
    def _route_format(self) -> str:
        return "artists/{id}/top-tracks"
