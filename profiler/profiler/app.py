from datetime import datetime
import grpc
import pandas
from profiler.adapters.aggregations_repository.pg_aggregations_repository import (
    PgAggregationsRepository,
)

from profiler.adapters.metrics_repository.pg_metrics_repository import (
    PgMetricsRepository,
)
from profiler.adapters.models_repository.pg_models_repository import PgModelsRepository

from profiler.adapters.overall_reports_repo.pg_overall_reports_repository import (
    PgOverallReportsRepository,
)
from profiler.adapters.reports_repository.pg_reports_repository import (
    PgReportsRepository,
)
from profiler.resources.db.postgres.db_migration import run_migrations

from profiler.domain.model import Model
from profiler.grpc.monitoring_manager import MonitoringDataSubscriber
from profiler.protobuf.monitoring_manager_pb2 import RegisterPluginRequest
from profiler.protobuf.monitoring_manager_pb2_grpc import PluginManagementServiceStub
from profiler.use_cases.aggregation_use_case import AggregationUseCase
from profiler.use_cases.overall_reports_use_case import OverallReportsUseCase
from profiler.use_cases import metrics_use_case, report_use_case
from profiler.domain.model_signature import (
    ModelSignature,
)

from profiler.config.config import config


import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from profiler.utils.decode_url import decode_url


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_repo = PgMetricsRepository()
models_repo = PgModelsRepository()
reports_repo = PgReportsRepository()
aggregations_repo = PgAggregationsRepository()
overall_reports_repository = PgOverallReportsRepository()

aggregation_use_case = AggregationUseCase(
    repo=aggregations_repo, models_repo=models_repo
)
metrics_use_case = metrics_use_case.MetricsUseCase(
    metrics_repo=metrics_repo,
)
report_use_case = report_use_case.ReportUseCase(
    models_repo=models_repo,
    metrics_use_case=metrics_use_case,
    reports_repo=reports_repo,
    agg_use_case=aggregation_use_case,
)
overall_reports_use_case = OverallReportsUseCase(repo=overall_reports_repository)

channel = grpc.insecure_channel(config.manager_addr)
monitoring_data_grpc = MonitoringDataSubscriber(
    channel, metrics_use_case, report_use_case, overall_reports_use_case, models_repo
)


app.mount(
    "/static",
    StaticFiles(directory="profiler/resources/static/profiler-fe"),
    name="static",
)


@app.get("/health")
def hello():
    return {}


@app.post("/model")
async def register_model(
    name: str = Form(...),
    version: int = Form(...),
    contract: UploadFile = File(...),
    training: UploadFile = File(...),
):

    df = pandas.read_csv(training.file)
    contract = ModelSignature.parse_raw(contract.file.read())

    model = Model(name=name, version=version, contract=contract)
    models_repo.save(model=model)
    metrics_use_case.generate_metrics(model=model, t_df=df)

    report = report_use_case.generate_report(model, "training", datetime.now(), df)
    overall_reports_use_case.generate_overall_report(report)

    return model


@app.post("/model/batch")
async def process_batch(
    model_name: str = Form(...),
    model_version: int = Form(...),
    batch_name: str = Form(...),
    batch: UploadFile = File(...),
):

    try:
        df = pandas.read_csv(batch.file)
        model = models_repo.get_by_name(model_name, model_version)
        report = report_use_case.generate_report(model, batch_name, datetime.now(), df)
        print("report generated")
        report_use_case.save_report(report)
        return f"Report for batch {batch_name} was generated "
    except Exception as e:
        print("error")
        print(e)


@app.get("/models")
async def get_models():
    return models_repo.get_all()


@app.get("/aggregation/{model_name}/{model_version}")
async def get_rep(model_name: str, model_version: int):
    return aggregation_use_case.get(model_name, model_version)


@app.get("/report/{model_name}/{model_version}/{encoded_file_url}")
async def get_report(model_name: str, model_version: int, encoded_file_url: str):
    url = decode_url(encoded_file_url)
    return report_use_case.get_report(model_name, model_version, url)


@app.get("/overall_report/{model_name}/{model_version}/{encoded_file_url}")
async def get_overall_report(
    model_name: str, model_version: int, encoded_file_url: str
):
    url = decode_url(encoded_file_url)
    return overall_reports_use_case.calculate_batch_stats(
        model_name=model_name, model_version=model_version, batch_name=url
    )


#  TODO (Pasha): add exceptions
if __name__ == "__main__":
    try:
        print(f"Independent mode: {config.profiler_independent_mode}")

        db_user = config.postgres_user
        db_password = config.postgres_password
        db_host = config.postgres_host
        db_port = config.postgres_port
        db_name = config.postgres_db

        run_migrations(
            "profiler/resources/db/postgres",
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        )

        if not config.profiler_independent_mode:
            plugin_manager = PluginManagementServiceStub(channel)

            registration_request = RegisterPluginRequest(
                plugin_id="profiler",
                description="Profiler plugin for inference data",
                routePath="profiler",
                ngModuleName="DashboardModule",
                remoteName="hydrosphereProfiler",
                exposedModule="./Module",
                addr=f"http://{config.http_host}:{config.http_port}",
            )
            print("Registering plugin...")
            registering = True
            while registering:
                try:
                    plugin_manager.RegisterPlugin(registration_request)
                    registering = False
                    print("Success")
                except Exception:
                    pass

            monitoring_data_grpc.start_watching()

        print("Start server...")
        uvicorn.run(app, host="0.0.0.0", port=config.http_port, log_level="info")
    except Exception as e:
        print("Could not start application")
        print(e)
