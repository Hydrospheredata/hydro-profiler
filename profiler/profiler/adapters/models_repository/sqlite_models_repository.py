from profiler.domain.model_signature import ModelSignature
from profiler.ports.models_repository import ModelsRepository
from profiler.domain.model import Model

import sqlite3


class SqliteModelsRepository(ModelsRepository):
    con = sqlite3.connect("profiler/resources/db/sqlite/profiler.db")
    cur = con.cursor()

    def get_all(self):
        self.cur.execute(
            "SELECT * FROM models"
        )
        res = []
        for (name, version, contract) in self.cur.fetchall():
            res.append(Model(name=name, version=version, contract=ModelSignature.parse_raw(contract)))

        return res

    def get_by_name(self, model_name: str, model_version: int) -> Model:
        self.cur.execute(
            "SELECT * FROM models WHERE name=? AND version=?", (model_name, model_version)
        )
        (name, version, contract) = self.cur.fetchone()
        return Model(name=name, version=version, contract=ModelSignature.parse_raw(contract))

    def save(self, model: Model):
        self.cur.execute(
            "INSERT INTO models VALUES (?, ?, ?)", (model.name, model.version, model.contract.json())
        )
        self.con.commit()
