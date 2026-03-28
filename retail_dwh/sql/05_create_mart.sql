-- Create a reporting mart layer for BI workloads.
CREATE SCHEMA IF NOT EXISTS mart;

DROP MATERIALIZED VIEW IF EXISTS mart.monthly_sales;

CREATE MATERIALIZED VIEW mart.monthly_sales AS
SELECT
    date_trunc('month', fs.sales_date)::date AS sales_month,
    dp.category,
    ds.store_type,
    COUNT(*) AS order_count,
    COUNT(DISTINCT fs.customer_sk) AS distinct_customers,
    SUM(fs.total_amount) AS total_sales,
    AVG(fs.total_amount) AS average_order_value
FROM fact_sales AS fs
JOIN dim_products AS dp
    ON fs.product_sk = dp.product_sk
JOIN dim_stores AS ds
    ON fs.store_sk = ds.store_sk
GROUP BY 1, 2, 3;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mart_monthly_sales_pk
    ON mart.monthly_sales (sales_month, category, store_type);
