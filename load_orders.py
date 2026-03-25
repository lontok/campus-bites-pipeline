"""Load campus_bites_orders.csv into the Postgres orders table."""

import csv
import psycopg2

# Connection settings for the Dockerized Postgres instance (see docker-compose.yml)
DB_CONFIG = {
    "host": "localhost",
    "port": 5435,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

CSV_PATH = "data/campus_bites_orders.csv"

# IF NOT EXISTS lets this script run even when the table already exists
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id           INTEGER PRIMARY KEY,
    order_date         DATE         NOT NULL,
    order_time         TIME         NOT NULL,
    customer_segment   VARCHAR(50)  NOT NULL,
    order_value        NUMERIC(10,2) NOT NULL,
    cuisine_type       VARCHAR(50)  NOT NULL,
    delivery_time_mins INTEGER,
    promo_code_used    BOOLEAN      NOT NULL,
    is_reorder         BOOLEAN      NOT NULL
);
"""

# ON CONFLICT DO NOTHING makes this idempotent -- re-running skips existing rows
INSERT_ROW = """
INSERT INTO orders (
    order_id, order_date, order_time, customer_segment,
    order_value, cuisine_type, delivery_time_mins,
    promo_code_used, is_reorder
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (order_id) DO NOTHING;
"""


# -- Type conversion helpers --
# The CSV stores booleans as "Yes"/"No" text and has some empty cells
# for delivery_time_mins and is_reorder. These helpers handle both cases.


def to_bool(value):
    """Convert Yes/No/empty to Python bool. Empty or missing defaults to False."""
    return value.strip().lower() == "yes" if value else False


def to_int_or_none(value):
    """Convert to int, or None if empty (for nullable integer columns)."""
    return int(value) if value.strip() else None


def main():
    # Read CSV and convert each row's types before inserting
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                int(row["order_id"]),
                row["order_date"],
                row["order_time"],
                row["customer_segment"],
                row["order_value"],
                row["cuisine_type"],
                to_int_or_none(row["delivery_time_mins"]),
                to_bool(row["promo_code_used"]),
                to_bool(row["is_reorder"]),
            )
            for row in reader
        ]

    # Connect, create table if needed, and batch-insert all rows
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE)
            cur.executemany(INSERT_ROW, rows)
        conn.commit()
        print(f"Loaded {len(rows)} rows into orders table.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
