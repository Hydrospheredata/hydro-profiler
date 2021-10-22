from abc import ABC
from abc import abstractmethod

from profiler.domain.model import Model


class ModelsRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_name(self, model_name: str, model_version: int) -> Model:
        pass

    @abstractmethod
    def save(self, model: Model):
        pass
