from typing import Type, Dict

from spotipyio.logic import EpisodesCollector
from spotipyio.contract import BaseManager, ISpotifyComponent


class EpisodesManager(BaseManager):
    def __init__(self, info: EpisodesCollector):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": EpisodesCollector,
        }
