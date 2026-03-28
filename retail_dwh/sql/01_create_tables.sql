-- =============================================
-- Retail DWH Schema: Dimension & Fact Tables
-- =============================================

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_sk          INTEGER PRIMARY KEY,
    customer_id          VARCHAR(50),
    first_name           VARCHAR(100),
    last_name            VARCHAR(100),
    email                VARCHAR(200),
    residential_location VARCHAR(200),
    customer_segment     VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_sk      INTEGER PRIMARY KEY,
    product_id      VARCHAR(50),
    product_name    VARCHAR(200),
    category        VARCHAR(100),
    brand           VARCHAR(100),
    origin_location VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS dim_stores (
    store_sk         INTEGER PRIMARY KEY,
    store_id         VARCHAR(50),
    store_name       VARCHAR(200),
    store_type       VARCHAR(100),
    store_location   VARCHAR(200),
    store_manager_sk INTEGER
);

CREATE TABLE IF NOT EXISTS dim_salespersons (
    salesperson_sk   INTEGER PRIMARY KEY,
    salesperson_id   VARCHAR(50),
    salesperson_name VARCHAR(200),
    salesperson_role VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_campaigns (
    campaign_sk      INTEGER PRIMARY KEY,
    campaign_id      VARCHAR(50),
    campaign_name    VARCHAR(200),
    start_date_sk    INTEGER,
    end_date_sk      INTEGER,
    campaign_budget  NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS dim_dates (
    full_date  DATE,
    date_sk    INTEGER PRIMARY KEY,
    year       INTEGER,
    month      INTEGER,
    day        INTEGER,
    weekday    INTEGER,
    quarter    INTEGER
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_sk        INTEGER PRIMARY KEY,
    sales_id        VARCHAR(50) NOT NULL,
    customer_sk     INTEGER REFERENCES dim_customers(customer_sk),
    product_sk      INTEGER REFERENCES dim_products(product_sk),
    store_sk        INTEGER REFERENCES dim_stores(store_sk),
    salesperson_sk  INTEGER REFERENCES dim_salespersons(salesperson_sk),
    campaign_sk     INTEGER REFERENCES dim_campaigns(campaign_sk),
    sales_date      TIMESTAMP,
    total_amount    NUMERIC(12,2)
);
