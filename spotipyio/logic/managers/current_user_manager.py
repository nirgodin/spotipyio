from typing import Type, Dict

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.collectors.current_profile_collector import CurrentProfileCollector
from spotipyio.logic.collectors.top_items_collectors.top_items_collector import TopItemsCollector


class CurrentUserManager(BaseManager):
    def __init__(self, top_items: TopItemsCollector, profile: CurrentProfileCollector):
        super().__init__()
        self.top_items = top_items
        self.profile = profile

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "top_items": TopItemsCollector,
            "profile": CurrentProfileCollector
        }
