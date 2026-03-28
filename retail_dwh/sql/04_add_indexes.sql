-- Add indexes to improve join and filter performance on the fact table.
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_sk
    ON fact_sales (customer_sk);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product_sk
    ON fact_sales (product_sk);

CREATE INDEX IF NOT EXISTS idx_fact_sales_store_sk
    ON fact_sales (store_sk);

CREATE INDEX IF NOT EXISTS idx_fact_sales_salesperson_sk
    ON fact_sales (salesperson_sk);

CREATE INDEX IF NOT EXISTS idx_fact_sales_campaign_sk
    ON fact_sales (campaign_sk);

CREATE INDEX IF NOT EXISTS idx_fact_sales_sales_date
    ON fact_sales (sales_date);
