FROM apache/superset:latest

USER root

# Install PostgreSQL driver into the virtual environment used by Superset.
# We use --target because the global pip does not install into the venv by default.
RUN pip install --target $(python -c "import site; print(site.getsitepackages()[0])") psycopg2-binary

USER superset
