from abc import abstractmethod
from typing import Dict, Type

from pytest_httpserver import HTTPServer

from spotipyio.testing.infra.base_test_component import BaseTestComponent


class BaseTestManager:
    def __init__(self, **named_component: Dict[str, BaseTestComponent]):
        pass

    @classmethod
    def create(cls, server: HTTPServer) -> "BaseManager":
        named_components = {}

        for name, component in cls._components().items():
            named_components[name] = component(server=server)

        return cls(**named_components)

    @staticmethod
    @abstractmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        raise NotImplementedError
