from typing import Type, Dict

from spotipyio import ChaptersCollector
from spotipyio.contract import BaseManager, ISpotifyComponent


class ChaptersManager(BaseManager):
    def __init__(self, info: ChaptersCollector):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": ChaptersCollector,
        }
