from abc import ABC, abstractmethod
from typing import Type, Dict

from aiohttp import ClientSession

from spotipyio.contract.collectors.base_collector import BaseCollector


class BaseManager(ABC):
    def __init__(self, **named_collectors: Dict[str, BaseCollector]):
        pass

    @classmethod
    def create(cls, session: ClientSession) -> "BaseManager":
        named_collectors = {}

        for name, collector in cls._collectors().items():
            named_collectors[name] = collector(session)

        return cls(**named_collectors)

    @staticmethod
    @abstractmethod
    def _collectors() -> Dict[str, Type[BaseCollector]]:
        raise NotImplementedError
