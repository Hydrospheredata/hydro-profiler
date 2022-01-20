import logging
from alembic.config import Config
from alembic import command


def run_migrations(script_location: str, dsn: str) -> None:
    logging.info(f"Running DB migrations in {script_location} on {dsn}")
    alembic_cfg = Config("profiler/resources/db/postgres/alembic.ini")
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    logging.info("config ok")
    command.upgrade(alembic_cfg, "heads")
    logging.info("Migrated")
