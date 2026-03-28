"""
Create and run a Great Expectations suite for the fact_sales table.
"""
import os

import great_expectations as gx
from great_expectations.core.expectation_configuration import ExpectationConfiguration


GX_CONTEXT_ROOT = os.getenv("GX_CONTEXT_ROOT", "/app/great_expectations")
SUITE_NAME = "fact_sales_suite"
CHECKPOINT_NAME = "fact_sales_checkpoint"
DATASOURCE_NAME = "retail_dwh_postgres"
DATA_ASSET_NAME = "public.fact_sales"


context = gx.get_context(context_root_dir=GX_CONTEXT_ROOT)

try:
    context.delete_expectation_suite(SUITE_NAME)
except Exception:
    pass

suite = context.add_expectation_suite(expectation_suite_name=SUITE_NAME)

expectations = [
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "sales_sk"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "sales_id"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "customer_sk"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "product_sk"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "store_sk"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "salesperson_sk"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "campaign_sk"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "total_amount", "min_value": 0},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_unique",
        kwargs={"column": "sales_id"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "sales_date"},
    ),
    ExpectationConfiguration(
        expectation_type="expect_table_columns_to_match_set",
        kwargs={
            "column_set": [
                "sales_sk",
                "sales_id",
                "customer_sk",
                "product_sk",
                "store_sk",
                "salesperson_sk",
                "campaign_sk",
                "sales_date",
                "total_amount",
            ]
        },
    ),
]

suite.add_expectation_configurations(expectations)
context.save_expectation_suite(suite)
print(
    f"[OK] Expectation suite '{SUITE_NAME}' created with {len(expectations)} expectations."
)

checkpoint_config = {
    "name": CHECKPOINT_NAME,
    "config_version": 1,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": {
                "datasource_name": DATASOURCE_NAME,
                "data_connector_name": "default_inferred_data_connector",
                "data_asset_name": DATA_ASSET_NAME,
            },
            "expectation_suite_name": SUITE_NAME,
        }
    ],
}

try:
    context.delete_checkpoint(CHECKPOINT_NAME)
except Exception:
    pass

checkpoint = context.add_checkpoint(**checkpoint_config)
print(f"[OK] Checkpoint '{CHECKPOINT_NAME}' created.")

print("[INFO] Running validation...")
result = checkpoint.run()

if result.success:
    print("[OK] All validations passed.")
else:
    print("[WARN] Some validations failed. Check Data Docs for details.")

context.build_data_docs()
print("[OK] Data Docs generated.")
print("[INFO] Open: great_expectations/uncommitted/data_docs/local_site/index.html")
