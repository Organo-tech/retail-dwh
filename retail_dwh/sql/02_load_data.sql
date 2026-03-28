-- =============================================
-- Load CSV data into tables
-- =============================================
--
-- This script is designed for the Docker Compose workflow in this repository.
-- The host folder ./data is mounted into the Postgres container as /data.

COPY dim_customers(customer_sk, customer_id, first_name, last_name, email, residential_location, customer_segment)
FROM '/data/dim_customers.csv'
DELIMITER ',' CSV HEADER;

COPY dim_products(product_sk, product_id, product_name, category, brand, origin_location)
FROM '/data/dim_products.csv'
DELIMITER ',' CSV HEADER;

COPY dim_stores(store_sk, store_id, store_name, store_type, store_location, store_manager_sk)
FROM '/data/dim_stores.csv'
DELIMITER ',' CSV HEADER;

COPY dim_salespersons(salesperson_sk, salesperson_id, salesperson_name, salesperson_role)
FROM '/data/dim_salespersons.csv'
DELIMITER ',' CSV HEADER;

COPY dim_campaigns(campaign_sk, campaign_id, campaign_name, start_date_sk, end_date_sk, campaign_budget)
FROM '/data/dim_campaigns.csv'
DELIMITER ',' CSV HEADER;

COPY dim_dates(full_date, date_sk, year, month, day, weekday, quarter)
FROM '/data/dim_dates.csv'
DELIMITER ',' CSV HEADER;

COPY fact_sales(sales_sk, sales_id, customer_sk, product_sk, store_sk, salesperson_sk, campaign_sk, sales_date, total_amount)
FROM '/data/fact_sales_normalized.csv'
DELIMITER ',' CSV HEADER;
