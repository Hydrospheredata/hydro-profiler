from ports.reports_repository import ReportsRepository
from domain.production_batch import ProductionBatch
from domain.model import Model
import json


class LocalReportsRepository(ReportsRepository):
    def get_report(self, model_name: str, batch: str):
        return super().get_report(model_name, batch)

    def save(self, model_name: str, batch_name: str, report: list):
        file = f"resources/{model_name}_{batch_name}_report.json"

        with open(file, "w") as f:
            f.write(json.dumps(report))
