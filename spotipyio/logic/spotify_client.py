from aiohttp import ClientSession

from spotipyio.logic.collectors.artists_collector import ArtistsCollector


class SpotifyClient:
    def __init__(self, artists_collector: ArtistsCollector):
        self.artists = artists_collector

    @classmethod
    def create(cls, session: ClientSession) -> "SpotifyClient":
        return SpotifyClient(
            artists_collector=ArtistsCollector(session)
        )
