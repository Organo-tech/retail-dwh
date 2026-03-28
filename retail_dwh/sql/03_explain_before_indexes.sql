-- Benchmark query before adding indexes.
EXPLAIN ANALYZE
SELECT
    date_trunc('month', fs.sales_date)::date AS sales_month,
    dp.category,
    ds.store_type,
    COUNT(*) AS order_count,
    SUM(fs.total_amount) AS total_sales
FROM fact_sales AS fs
JOIN dim_products AS dp
    ON fs.product_sk = dp.product_sk
JOIN dim_stores AS ds
    ON fs.store_sk = ds.store_sk
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;
