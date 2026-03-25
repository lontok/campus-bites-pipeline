# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A local Postgres database for interactive SQL analysis of campus food delivery orders. The database runs in Docker; a Python script handles data loading from CSV.

## Common commands

```bash
# Start the database
docker compose up -d

# Stop (data persists)
docker compose down

# Full reset (wipe volume, reload from scratch)
docker compose down -v && docker compose up -d

# Load/reload CSV data into the database
source .venv/bin/activate
python load_orders.py

# Connect to the database interactively
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

## How data loading works

There is no init.sql. The Docker container starts with an empty `campus_bites` database, and `load_orders.py` handles everything:

1. Creates the `orders` table if it doesn't exist
2. Reads `data/campus_bites_orders.csv` with type conversions (Yes/No to boolean, empty strings to NULL for nullable integers)
3. Inserts rows with `ON CONFLICT DO NOTHING`, so the script is idempotent

The CSV has data quality quirks: some rows have empty `is_reorder` and `delivery_time_mins` fields. The type helpers `to_bool` and `to_int_or_none` handle these.

## Database connection

- Host: localhost, Port: 5435, Database: campus_bites, User/Password: postgres/postgres
- Port 5435 is used to avoid conflicts with any local Postgres on 5432

## Python environment

- Virtual environment at `.venv/`
- Single dependency: `psycopg2-binary`
- Install: `pip install -r requirements.txt`
