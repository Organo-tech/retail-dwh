#!/bin/sh
set -eu

python /app/pythonpath/ensure_metadata_db.py

superset db upgrade

if ! superset fab create-admin \
  --username "${SUPERSET_ADMIN_USERNAME}" \
  --firstname "${SUPERSET_ADMIN_FIRSTNAME}" \
  --lastname "${SUPERSET_ADMIN_LASTNAME}" \
  --email "${SUPERSET_ADMIN_EMAIL}" \
  --password "${SUPERSET_ADMIN_PASSWORD}"; then
  echo "Superset admin user already exists or could not be created automatically."
fi

superset init

python /app/pythonpath/provision_assets.py

exec superset run -h 0.0.0.0 -p 8088
