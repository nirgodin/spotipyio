from abc import ABC, abstractmethod
from typing import Type, Dict

from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession


class BaseManager(ABC):
    def __init__(self, **named_component: Dict[str, ISpotifyComponent]):
        pass

    @classmethod
    def create(cls, session: SpotifySession) -> "BaseManager":
        named_components = {}

        for name, component in cls._components().items():
            named_components[name] = component(session)

        return cls(**named_components)

    @staticmethod
    @abstractmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        raise NotImplementedError
