import json
import os
import uuid

from superset.app import create_app


def build_dashboard_layout(chart_id: int, chart_uuid: str, chart_name: str) -> str:
    row_id = f"ROW-{uuid.uuid4().hex[:10]}"
    chart_container_id = f"CHART-{uuid.uuid4().hex[:10]}"
    position = {
        "DASHBOARD_VERSION_KEY": "v2",
        "ROOT_ID": {
            "id": "ROOT_ID",
            "type": "ROOT",
            "children": ["GRID_ID"],
        },
        "GRID_ID": {
            "id": "GRID_ID",
            "type": "GRID",
            "parents": ["ROOT_ID"],
            "children": [row_id],
        },
        row_id: {
            "id": row_id,
            "type": "ROW",
            "parents": ["ROOT_ID", "GRID_ID"],
            "children": [chart_container_id],
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
        },
        chart_container_id: {
            "id": chart_container_id,
            "type": "CHART",
            "parents": ["ROOT_ID", "GRID_ID", row_id],
            "children": [],
            "meta": {
                "chartId": chart_id,
                "uuid": chart_uuid,
                "sliceName": chart_name,
                "height": 50,
                "width": 12,
            },
        },
    }
    return json.dumps(position)


app = create_app()

with app.app_context():
    from flask_appbuilder.security.sqla.models import User

    from superset import db
    from superset.connectors.sqla.models import SqlMetric, SqlaTable
    from superset.models.core import Database
    from superset.models.dashboard import Dashboard
    from superset.models.slice import Slice

    admin_user = (
        db.session.query(User)
        .filter_by(username=os.environ["SUPERSET_ADMIN_USERNAME"])
        .one()
    )

    bi_uri = (
        f"postgresql+psycopg2://{os.environ['BI_VIEWER_USER']}:"
        f"{os.environ['BI_VIEWER_PASSWORD']}@postgres:5432/{os.environ['POSTGRES_DB']}"
    )

    database = (
        db.session.query(Database)
        .filter_by(database_name="warehouse_bi_viewer")
        .one_or_none()
    )
    if database is None:
        database = Database(
            database_name="warehouse_bi_viewer",
            sqlalchemy_uri=bi_uri,
            expose_in_sqllab=True,
            allow_run_async=False,
            allow_ctas=False,
            allow_cvas=False,
            allow_dml=False,
        )
        db.session.add(database)
        db.session.commit()
    else:
        database.sqlalchemy_uri = bi_uri
        db.session.add(database)
        db.session.commit()

    dataset = (
        db.session.query(SqlaTable)
        .filter_by(database_id=database.id, schema="mart", table_name="monthly_sales")
        .one_or_none()
    )
    if dataset is None:
        dataset = SqlaTable(
            table_name="monthly_sales",
            schema="mart",
            database_id=database.id,
            main_dttm_col="sales_month",
        )
        dataset.owners = [admin_user]
        db.session.add(dataset)
        db.session.commit()

    dataset.fetch_metadata()
    dataset.main_dttm_col = "sales_month"
    dataset.owners = [admin_user]

    if not any(metric.metric_name == "sum__total_sales" for metric in dataset.metrics):
        dataset.metrics.append(
            SqlMetric(
                metric_name="sum__total_sales",
                verbose_name="Total Sales",
                metric_type="sum",
                expression="SUM(total_sales)",
            )
        )

    if not any(metric.metric_name == "sum__order_count" for metric in dataset.metrics):
        dataset.metrics.append(
            SqlMetric(
                metric_name="sum__order_count",
                verbose_name="Order Count",
                metric_type="sum",
                expression="SUM(order_count)",
            )
        )

    db.session.add(dataset)
    db.session.commit()

    chart_name = "Monthly Sales Mart Table"
    chart = db.session.query(Slice).filter_by(slice_name=chart_name).one_or_none()

    chart_params = {
        "datasource": f"{dataset.id}__table",
        "viz_type": "table",
        "query_mode": "raw",
        "all_columns": [
            "sales_month",
            "category",
            "store_type",
            "total_sales",
            "order_count",
            "distinct_customers",
            "average_order_value",
        ],
        "order_desc": True,
        "row_limit": 100,
        "server_page_length": 10,
        "table_timestamp_format": "smart_date",
        "adhoc_filters": [],
    }

    if chart is None:
        chart = Slice(
            slice_name=chart_name,
            datasource_id=dataset.id,
            datasource_type="table",
            datasource_name="mart.monthly_sales",
            viz_type="table",
            params=json.dumps(chart_params),
            query_context=None,
            owners=[admin_user],
        )
        db.session.add(chart)
        db.session.commit()
    else:
        chart.datasource_id = dataset.id
        chart.datasource_type = "table"
        chart.datasource_name = "mart.monthly_sales"
        chart.viz_type = "table"
        chart.params = json.dumps(chart_params)
        chart.owners = [admin_user]
        db.session.add(chart)
        db.session.commit()

    chart_uuid = str(getattr(chart, "uuid", uuid.uuid4()))

    dashboard_name = "Retail Sales Performance Dashboard"
    dashboard = (
        db.session.query(Dashboard)
        .filter_by(dashboard_title=dashboard_name)
        .one_or_none()
    )

    position_json = build_dashboard_layout(chart.id, chart_uuid, chart_name)

    if dashboard is None:
        dashboard = Dashboard(
            dashboard_title=dashboard_name,
            slug="retail-sales-performance-dashboard",
            published=True,
            json_metadata=json.dumps({}),
            position_json=position_json,
            owners=[admin_user],
            slices=[chart],
        )
        db.session.add(dashboard)
    else:
        dashboard.slug = "retail-sales-performance-dashboard"
        dashboard.published = True
        dashboard.position_json = position_json
        dashboard.json_metadata = json.dumps({})
        dashboard.owners = [admin_user]
        dashboard.slices = [chart]
        db.session.add(dashboard)

    db.session.commit()
