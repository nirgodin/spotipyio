from spotipyio.contract.collectors.base_single_collector import BaseSingleCollector


class ArtistsTopTracksCollector(BaseSingleCollector):
    @property
    def _route_format(self) -> str:
        return "artists/{id}/top-tracks"
