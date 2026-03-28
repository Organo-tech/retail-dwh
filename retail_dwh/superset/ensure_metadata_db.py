import os
import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def ensure_metadata_db() -> None:
    max_attempts = int(os.getenv("SUPERSET_DB_CONNECT_RETRIES", "30"))
    retry_delay = int(os.getenv("SUPERSET_DB_CONNECT_DELAY_SECONDS", "2"))
    connection = None

    for attempt in range(1, max_attempts + 1):
        try:
            connection = psycopg2.connect(
                dbname="postgres",
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                host="postgres",
                port=5432,
            )
            break
        except psycopg2.OperationalError:
            if attempt == max_attempts:
                raise
            print(
                f"Postgres is not ready for Superset metadata bootstrap yet. "
                f"Retrying ({attempt}/{max_attempts})..."
            )
            time.sleep(retry_delay)

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    metadata_db = os.environ["SUPERSET_METADATA_DB"]

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (metadata_db,),
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE "{metadata_db}"')

    connection.close()


if __name__ == "__main__":
    ensure_metadata_db()
