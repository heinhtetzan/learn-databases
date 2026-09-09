← [2.16 Views](16-views.md)

# 2.17 Create Tables: More Examples

[Lesson 2.2](02-your-first-database-apple-example.md) taught `CREATE TABLE`
with one example: `products`. Real projects need many different table
shapes. Let's practice with several more — each one highlighting a technique
you haven't seen yet.

## Step 1 — `IF NOT EXISTS`: safe to re-run

Setup scripts often get run more than once. Without `IF NOT EXISTS`, running
the same `CREATE TABLE` twice errors out the second time:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    task_id     SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    is_done     BOOLEAN NOT NULL DEFAULT FALSE,
    due_date    DATE,
    priority    TEXT NOT NULL DEFAULT 'medium'
                CHECK (priority IN ('low', 'medium', 'high'))
);
```

`CHECK (priority IN (...))` is a lightweight stand-in for a proper `ENUM`
type — restricting `priority` to exactly 3 allowed values, no misspellings.

```sql
INSERT INTO tasks (title, due_date, priority) VALUES
    ('Restock AirPods Max', '2026-04-01', 'high'),
    ('Update store hours page', NULL, 'low');
```

## Step 2 — A fresh domain: a small blog

New domain, same skills from [Lesson 2.10](10-relationships-and-foreign-keys.md):

```sql
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name      TEXT NOT NULL
);

CREATE TABLE posts (
    post_id       SERIAL PRIMARY KEY,
    author_id     INTEGER NOT NULL REFERENCES authors(author_id),
    title         TEXT NOT NULL,
    slug          TEXT NOT NULL UNIQUE,   -- URL-friendly identifier, e.g. "hello-world"
    body          TEXT NOT NULL,
    published_at  TIMESTAMP    -- NULL means "still a draft"
);
```

`published_at` being nullable is a deliberate design choice: `NULL` means
"not published yet," rather than adding a separate `is_published BOOLEAN`
column that could disagree with the actual publish date.

```sql
INSERT INTO authors (name) VALUES ('Priya Patel');
INSERT INTO posts (author_id, title, slug, body, published_at) VALUES
    (1, 'Hello World', 'hello-world', 'Our first post!', '2026-03-01 09:00:00'),
    (1, 'Upcoming Sale', 'upcoming-sale', 'Draft — details TBD', NULL);
```

## Step 3 — Referencing a table from an earlier lesson

New tables don't have to stand alone — `warehouses` and `inventory` here
track *where* our existing `products` (from Part 1) are physically stocked:

```sql
CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    city         TEXT NOT NULL
);

CREATE TABLE inventory (
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
    product_id   INTEGER REFERENCES products(product_id),  -- reuses Lesson 2.2's table
    quantity     INTEGER NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (warehouse_id, product_id)   -- composite key, from Lesson 2.13
);
```

```sql
INSERT INTO warehouses (city) VALUES ('Austin'), ('Newark');
INSERT INTO inventory (warehouse_id, product_id, quantity) VALUES
    (1, 1, 120),   -- 120 iPhone 17 Pro in Austin
    (2, 1, 80);    -- 80 iPhone 17 Pro in Newark
```

## Step 4 — `CREATE TABLE AS`: snapshot a query into a real table

[Lesson 2.16](16-views.md)'s views stay **live** — re-run the underlying
query every time. `CREATE TABLE ... AS` instead **freezes** a query's result
into a brand new, independent table, as of right now:

```sql
CREATE TABLE products_snapshot_2026_q1 AS
SELECT * FROM products;
```

Later changes to `products` — a price update, a new product — **never**
touch `products_snapshot_2026_q1` again; it's a genuine copy, not a saved
query. Useful for "what did our catalog look like at the end of Q1?"
reporting, where you specifically want the past preserved, not the present.

## Step 5 — Temporary tables: scratch work that cleans itself up

```sql
CREATE TEMP TABLE price_check AS
SELECT product_id, name, price FROM products WHERE price > 1000;

SELECT * FROM price_check;   -- use it like any table, for the rest of this session
```

A `TEMP` table exists only for your current database session — close the
connection, and PostgreSQL drops it automatically. Handy for a multi-step
script's intermediate results, without leaving cleanup tables behind in your
real schema.

## Step 6 — Recap: every `CREATE TABLE` technique so far

| Technique | Where you've seen it |
|---|---|
| Basic columns + types | [Lesson 2.2](02-your-first-database-apple-example.md) |
| `PRIMARY KEY`, `REFERENCES`, `CHECK`, `UNIQUE`, `DEFAULT` | [Lesson 2.13](13-constraints.md) |
| Composite `PRIMARY KEY` | [Lesson 2.10](10-relationships-and-foreign-keys.md), Step 3 above |
| `IF NOT EXISTS` | Step 1 above |
| Nullable column as a meaningful state (not just "missing data") | Step 2 above |
| Referencing a table from a different lesson/domain | Step 3 above |
| `CREATE TABLE ... AS` (snapshot, not live) | Step 4 above |
| `CREATE TEMP TABLE` (session-scoped) | Step 5 above |

---
← [2.16 Views](16-views.md) | Next: [2.18 User & Access Management →](18-user-access-management.md)
