# Architecture Diagram

```mermaid
flowchart LR
    A[Kaggle CSV Files] --> B[PostgreSQL Warehouse]
    B --> C[Dimension Tables]
    B --> D[fact_sales]
    D --> E[Indexes on join keys and sales_date]
    D --> F[Reporting Mart: mart.monthly_sales]
    B --> G[Great Expectations Validation]
    F --> H[Apache Superset Dashboard]
    E --> H
    G --> I[Data Docs]

    subgraph Docker Compose Stack
        B
        G
        H
    end
```

## Summary

The project flow is:

1. Raw CSV files are mounted into the Postgres container.
2. SQL bootstrap scripts create the warehouse schema and load the source data.
3. Indexes improve access paths on the transactional fact table.
4. `mart.monthly_sales` materializes reporting-ready monthly aggregates.
5. Great Expectations validates warehouse quality and generates Data Docs.
6. Apache Superset connects through the read-only `bi_viewer` user and serves dashboard visualizations.
