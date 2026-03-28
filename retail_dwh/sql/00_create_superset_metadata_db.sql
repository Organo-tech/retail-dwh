-- Create a dedicated metadata database for Apache Superset.
-- This script runs only during the first Postgres initialization.
SELECT 'CREATE DATABASE superset_meta'
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'superset_meta'
)\gexec
