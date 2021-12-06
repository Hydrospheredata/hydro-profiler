import grpc
from yoyo.backends import DatabaseBackend
import pandas
import yoyo
import os

from profiler.adapters.aggregations_repository.sqlite_aggregations_repository import (
    SqliteAggregationsRepository,
)
from profiler.adapters.models_repository.sqlite_models_repository import (
    SqliteModelsRepository,
)
from profiler.adapters.reports_repository.sqlite_reports_repository import (
    SqliteReportsRepository,
)
from profiler.adapters.metrics_repository.sqlite_metrics_repository import (
    SqliteMetricsRepository,
)

from profiler.adapters.overall_reports_repo.sqlite_overall_reports_repository import (
    SqliteOverallReportsRepository,
)

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

metrics_repo = SqliteMetricsRepository()
models_repo = SqliteModelsRepository()
reports_repo = SqliteReportsRepository()
aggregations_repo = SqliteAggregationsRepository()
overall_reports_repository = SqliteOverallReportsRepository()

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
    agg_use_case=aggregation_use_case,
)
overall_reports_use_case = OverallReportsUseCase(
    overall_reports_repo=overall_reports_repository
)

channel = grpc.insecure_channel(config.manager_addr)
monitoring_data_grpc = MonitoringDataSubscriber(
    channel, metrics_use_case, report_use_case, overall_reports_use_case
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

    report = report_use_case.generate_report(model=model, batch_name="training", df=df)
    overall_reports_use_case.generate_overall_report(
        model_name=name,
        model_version=version,
        batch_name="training",
        report=report,
    )

    return model


@app.post("/model/batch")
async def process_batch(
    model_name: str = Form(...),
    model_version: int = Form(...),
    batch_name: str = Form(...),
    batch: UploadFile = File(...),
):
    df = pandas.read_csv(batch.file)
    model = models_repo.get_by_name(model_name, model_version)
    report = report_use_case.generate_report(model=model, batch_name=batch_name, df=df)
    report_use_case.save_report(model, batch_name, report)

    overall_reports_use_case.generate_overall_report(
        model_name=model_name,
        model_version=model_version,
        batch_name=batch_name,
        report=report,
    )

    return f"Report for batch {batch_name} was generated "


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


def migrate(db_uri, migrations_path):
    print("Start migrations")
    parsed_uri = yoyo.connections.parse_uri(db_uri)
    scheme, _, _, _, _, database, _ = parsed_uri
    if scheme == "sqlite":
        directory = os.path.dirname(database)
        if not os.path.exists(directory):
            os.makedirs(directory)
    try:
        connection: DatabaseBackend = yoyo.get_backend(db_uri)
        migrations = yoyo.read_migrations(migrations_path)
        connection.apply_migrations(connection.to_apply(migrations))
    except Exception as e:
        print(e)


#  TODO (Pasha): add exceptions
if __name__ == "__main__":
    try:
        print(f"Independent mode: {config.profiler_independent_mode}")

        migrate(
            "sqlite:///profiler/resources/db/sqlite/profiler.db",
            "profiler/resources/db/sqlite/migrations",
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
