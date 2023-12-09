from spotipyio.consts.spotify_consts import PLAYLISTS
from spotipyio.contract.collectors.base_single_collector import BaseSingleCollector


class PlaylistsCollector(BaseSingleCollector):
    @property
    def _route_format(self) -> str:
        return f"{PLAYLISTS}/{{id}}"
