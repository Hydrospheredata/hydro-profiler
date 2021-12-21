from typing import List
from profiler.domain.model import Model
from profiler.ports.models_repository import ModelsRepository


class LocalModelsRepository(ModelsRepository):
    models: List[Model] = []

    def get_all(self):
        return self.models

    def get_by_name(self, model_name: str, model_version: int) -> Model:
        return [
            x
            for x in self.models
            if x.name == model_name and x.version == model_version
        ][0]

    def save(self, model: Model):
        self.models.append(model)
