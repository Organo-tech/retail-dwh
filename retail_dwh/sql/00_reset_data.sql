-- =============================================
-- Reset loaded warehouse data for manual reruns
-- =============================================
--
-- Use this script before rerunning 02_load_data.sql from DBeaver or another SQL client.
-- It removes table contents without dropping the schema, constraints, or indexes.

TRUNCATE TABLE
    fact_sales,
    dim_campaigns,
    dim_dates,
    dim_salespersons,
    dim_stores,
    dim_products,
    dim_customers
RESTART IDENTITY CASCADE;
