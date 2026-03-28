import os


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


POSTGRES_USER = _require_env("POSTGRES_USER")
POSTGRES_PASSWORD = _require_env("POSTGRES_PASSWORD")
SUPERSET_METADATA_DB = _require_env("SUPERSET_METADATA_DB")
SUPERSET_SECRET_KEY = _require_env("SUPERSET_SECRET_KEY")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@postgres:5432/{SUPERSET_METADATA_DB}"
)

SECRET_KEY = SUPERSET_SECRET_KEY

WTF_CSRF_ENABLED = True
TALISMAN_ENABLED = False
ROW_LIMIT = 5000
