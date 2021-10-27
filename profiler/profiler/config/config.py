from pydantic import BaseSettings


class Config(BaseSettings):
    http_host: str = "0.0.0.0"
    http_port: int = 5000

    minio_endpoint = "http://minio:9000"
    aws_access_key_id = "minioadmin"
    aws_secret_access_key = "minioadmin"

    manager_addr: str = "monitoring-manager:8081"

    class Config:
        case_sensitive = False


config = Config()