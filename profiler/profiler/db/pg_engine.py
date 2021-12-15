import sqlalchemy
from profiler.config.config import config


user = config.postgres_user
password = config.postgres_password
host = config.postgres_host
port = config.postgres_port
db = config.postgres_db

engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
