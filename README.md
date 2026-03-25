# Campus Bites Pipeline

A local Postgres database for analyzing campus food delivery orders. Load the CSV once, then query interactively with SQL or natural language tools.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/)

## Getting started

1. Clone the repo and cd into it:

```bash
git clone <repo-url>
cd campus-bites-pipeline
```

2. Start the database:

```bash
docker compose up -d
```

On first run this creates the `orders` table, loads the CSV (1,132 rows), and converts text fields to proper types (booleans, dates, numerics).

3. Connect and query:

```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

```sql
SELECT customer_segment,
       COUNT(*)                    AS total_orders,
       ROUND(AVG(order_value), 2)  AS avg_order_value
FROM orders
GROUP BY customer_segment
ORDER BY total_orders DESC;
```

## Schema

| Column | Type | Notes |
|---|---|---|
| order_id | INTEGER | Primary key |
| order_date | DATE | |
| order_time | TIME | |
| customer_segment | VARCHAR(50) | e.g. Grad Student, Off-Campus |
| order_value | NUMERIC(10,2) | Dollar amount |
| cuisine_type | VARCHAR(50) | e.g. Asian, Breakfast, Indian |
| delivery_time_mins | INTEGER | Nullable |
| promo_code_used | BOOLEAN | Converted from Yes/No |
| is_reorder | BOOLEAN | Converted from Yes/No |

## Connection details

| Setting  | Value        |
|----------|--------------|
| Host     | localhost    |
| Port     | 5435         |
| Database | campus_bites |
| User     | postgres     |
| Password | postgres     |

## Stopping and resetting

Stop the container (data persists):

```bash
docker compose down
```

Full reset, wipe the volume and reload from CSV:

```bash
docker compose down -v
docker compose up -d
```
