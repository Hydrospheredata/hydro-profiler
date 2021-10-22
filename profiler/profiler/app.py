import pandas
from profiler.adapters.aggregations_repository.sqlite_aggregations_repository import SqliteAggregationsRepository
from profiler.adapters.models_repository.sqlite_models_repository import SqliteModelsRepository
from profiler.adapters.reports_repository.sqlite_reports_repository import (
    SqliteReportsRepository,
)
from profiler.domain.model import Model
from profiler.use_cases.aggregation_use_case import AggregationUseCase
from profiler.use_cases import metrics_use_case, report_use_case
from profiler.domain.model_signature import ModelSignature, DataType, DataProfileType, ModelField
from profiler.adapters.metrics_repository.sqlite_metrics_repository import (
    SqliteMetricsRepository,
)

from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_repo = SqliteMetricsRepository()
models_repo = SqliteModelsRepository()
reports_repo = SqliteReportsRepository()
aggregations_repo = SqliteAggregationsRepository()


aggregation_use_case = AggregationUseCase(
    repo=aggregations_repo,
)
metrics_use_case = metrics_use_case.MetricsUseCase(
    metrics_repo=metrics_repo,
)
report_use_case = report_use_case.ReportUseCase(
    models_repo=models_repo,
    metrics_repo=metrics_repo,
    reports_repo=reports_repo,
    agg_use_case=aggregation_use_case
)

app.mount("/static", StaticFiles(directory="profiler/resources/static/profiler-fe"), name="static")

@app.post("/model")
async def register_model(
        name: str = Form(...),
        version: int = Form(...),
        contract: UploadFile = File(...),
        training: UploadFile = File(...)
):
    df = pandas.read_csv(training.file)
    contract = ModelSignature.parse_raw(contract.file.read())
    model = Model(name=name, version=version, contract=contract)
    models_repo.save(model=model)
    metrics_use_case.generate_metrics(model=model, t_df=df)

    return model


@app.post("/model/batch")
async def process_batch(
        model_name: str = Form(...),
        model_version: int = Form(...),
        batch_name: str = Form(...),
        batch: UploadFile = File(...)
):
    df = pandas.read_csv(batch.file)
    model = models_repo.get_by_name(model_name, model_version)
    report_use_case.generate_report(model=model, batch_name=batch_name, df=df)

    return f"Report for batch {batch_name} was generated "


@app.get("/models")
async def get_models():
    return models_repo.get_all()


@app.get("/aggregation/{model_name}/{model_version}")
async def get_rep(model_name: str, model_version: int):
    return aggregation_use_case.get(model_name=model_name, model_version=model_version)


@app.get("/report/{model_name}/{model_version}/{batch_name}")
async def get_report(model_name: str, model_version: int, batch_name: str):
    return report_use_case.get_report(model_name=model_name, model_version=model_version, batch_name=batch_name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
