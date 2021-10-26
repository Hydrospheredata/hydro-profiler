from pydantic import BaseSettings


class Config(BaseSettings):
    http_host: str = "0.0.0.0"
    http_port: int = 5000

    class Config:
        case_sensitive = False


config = Config()
