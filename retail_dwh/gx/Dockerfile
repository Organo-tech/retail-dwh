FROM python:3.11-slim
WORKDIR /app

RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --no-cache-dir \
    "great-expectations==0.18.21" \
    "sqlalchemy>=1.4,<2.0" \
    psycopg2-binary
