import os
from dataclasses import dataclass


@dataclass
class Config:
    database_url: str
    api_url: str
    db_timeout: int = 5
    api_timeout: float = 5.0


def load_config() -> Config:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    return Config(
        database_url=database_url,
        api_url=os.getenv("API_URL", "http://127.0.0.1:8000"),
        db_timeout=int(os.getenv("DB_TIMEOUT", "5")),
        api_timeout=float(os.getenv("API_TIMEOUT", "5")),
    )