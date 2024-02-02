from abc import ABC, abstractmethod
from typing import Any


class IEntityExtractor(ABC):
    @abstractmethod
    def extract(self, entity: Any) -> str:
        raise NotImplementedError
