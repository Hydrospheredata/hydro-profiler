from profiler.domain.model_signature import ModelSignature
from profiler.ports.models_repository import ModelsRepository
from profiler.domain.model import Model

from sqlalchemy import text
from profiler.db.pg_engine import engine


class PgModelsRepository(ModelsRepository):
    def get_all(self):
        with engine.connect() as conn:
            result = conn.execute("SELECT * FROM models").fetchall()
            models = []
            for (name, version, contract) in result:
                models.append(
                    Model(
                        name=name,
                        version=version,
                        contract=ModelSignature.parse_raw(contract),
                    )
                )

            return models

    def get_by_name(self, model_name: str, model_version: int) -> Model:
        with engine.connect as conn:
            query = text(
                "SELECT * FROM models WHERE name=:name AND version=:version"
            ).bindparams(name=model_name, version=model_version)

            (name, version, contract) = conn.execute(query).fetchone()

            return Model(
                name=name, version=version, contract=ModelSignature.parse_raw(contract)
            )

    def save(self, model: Model):
        with engine.connect() as conn:
            query = text(
                "INSERT INTO models VALUES (:name, :version, :contract)"
            ).bindparams(
                name=model.name, version=model.version, contract=model.contract.json()
            )
            conn.execute(query)
