# Dashboard Business Questions

## Dashboard Purpose

This dashboard is designed to give a quick but structured view of retail sales performance from the `mart.monthly_sales` layer.

The main purpose is to help users:

- monitor monthly business performance
- identify whether sales are growing or declining over time
- compare contribution across product categories
- compare contribution across store types
- inspect detailed monthly records behind the summary charts

## Primary Business Questions

The dashboard is intended to answer these business questions:

1. How is the business performing in the latest month?
   This is answered by the KPI cards:
   - Current Month Sales
   - Current Month Orders
   - Current Month Customers
   - Current Month AOV

2. Is sales performance trending up or down over time?
   This is answered by the `Monthly Sales Trend` line chart.

3. Which product categories contribute the most to total sales?
   This is answered by the `Sales by Category` bar chart.

4. Which store types contribute the most to total sales?
   This is answered by the `Sales by Store Type` treemap.

5. What are the detailed monthly records behind the summarized charts?
   This is answered by the `Monthly Sales Detail` table.

## Dashboard Components

### 1. KPI Cards

These KPI cards provide a snapshot of the latest month:

- Current Month Sales
- Current Month Orders
- Current Month Customers
- Current Month AOV

Business value:
- quickly shows current business health
- gives management an immediate monthly snapshot

### 2. Monthly Sales Trend

This line chart shows total sales by month.

Business value:
- highlights growth and decline patterns
- helps identify seasonality or unusual changes

### 3. Sales by Category

This chart compares total sales across product categories.

Business value:
- shows which categories drive revenue
- helps identify top-performing and weaker categories

### 4. Sales by Store Type

This treemap compares total sales across store types.

Business value:
- shows which sales channels or store formats contribute most
- helps assess channel mix and revenue concentration

### 5. Monthly Sales Detail

This table shows detailed records by:

- sales_month
- category
- store_type
- order_count
- distinct_customers
- total_sales
- average_order_value

Business value:
- supports drill-down and manual inspection
- helps validate the summary-level charts

## Recommended User Interaction

The dashboard becomes more useful when combined with filters such as:

- sales_month
- category
- store_type

With filters, users can answer more focused questions such as:

- How did Electronics perform in the latest quarter?
- Which store type performed best in a selected month?
- How does category contribution change after filtering to one store type?

## Scope and Limitations

This dashboard currently focuses on descriptive monitoring, not advanced period-over-period comparison.

It answers:

- what is happening now
- how performance changes over time
- where revenue comes from

It does not yet directly answer:

- month-over-month growth
- year-over-year growth
- target vs actual performance

To answer those questions more directly, the mart layer should be extended with fields such as:

- previous_month_sales
- mom_growth_pct
- previous_year_sales
- yoy_growth_pct

## Summary

This dashboard is suitable as a portfolio-ready analytical dashboard because it gives:

- executive-level KPI visibility
- trend monitoring
- category and channel comparison
- drill-down detail in one place

It is best positioned as a retail sales performance dashboard for monthly monitoring and business review.
