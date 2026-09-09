← [2.3 Types of SQL Queries](03-types-of-sql-queries.md)

# 2.4 Data Types in PostgreSQL

Every column you create needs a **data type** — you've already picked a few
without much explanation in [Lesson 2.2](02-your-first-database-apple-example.md)
(`TEXT`, `DECIMAL(10,2)`, `INTEGER`, `TIMESTAMP`). Let's slow down and look at
what's actually available, and an important reminder about switching engines.

## Step 1 — What a data type actually controls

A column's type controls 3 things at once:
1. **What values are allowed** — a `BOOLEAN` column can only ever hold
   true/false; it will reject the text `"maybe"`.
2. **How it's stored** — an `INTEGER` takes a fixed 4 bytes; a `TEXT` value's
   size depends on its length.
3. **What operations make sense** — you can do math on `DECIMAL`, but not on
   `TEXT`; you can compare `DATE`s chronologically, but not two arbitrary
   pieces of text that way.

## Step 2 — PostgreSQL's data types, grouped

![PostgreSQL Data Types, Grouped](../assets/images/postgres-data-types.png)

### Numeric

| Type | Use for |
|---|---|
| `INTEGER` | Whole numbers, everyday range (stock counts, ages) |
| `BIGINT` | Whole numbers, very large range |
| `DECIMAL(p,s)` / `NUMERIC(p,s)` | Exact decimal numbers — **always use for money** |
| `SERIAL` | Auto-incrementing integer — what we used for `product_id` |

### Text

| Type | Use for |
|---|---|
| `TEXT` | Any length of text, no limit — the simplest default choice |
| `VARCHAR(n)` | Text capped at `n` characters |
| `CHAR(n)` | Fixed-length text, padded with spaces — rarely needed today |

### Boolean

| Type | Use for |
|---|---|
| `BOOLEAN` | `TRUE` / `FALSE` values only |

### Date / Time

| Type | Use for |
|---|---|
| `DATE` | A calendar date only, no time (e.g., a birthday) |
| `TIME` | A time only, no date |
| `TIMESTAMP` | Date + time together — what we used for `created_at`/`updated_at` |
| `TIMESTAMPTZ` | Date + time, timezone-aware — usually the *safer* real-world choice |
| `INTERVAL` | A span of time (e.g., "3 days", "2 hours") |

### PostgreSQL-Special

| Type | Use for |
|---|---|
| `UUID` | A globally unique ID, not just unique within one table |
| `JSONB` | Structured, flexible data stored inside a relational column (bridges to [Module 07 NoSQL concepts](../01-fundamentals/03-types-of-databases.md)) |
| `ARRAY` | A list of values in a single column |
| `ENUM` | A fixed, named set of allowed values (e.g., `'small', 'medium', 'large'`) |

## Step 3 — Back to our products table

```sql
CREATE TABLE products (
    product_id  SERIAL PRIMARY KEY,        -- Numeric
    name        TEXT NOT NULL,             -- Text
    category    TEXT NOT NULL,             -- Text
    price       DECIMAL(10,2) NOT NULL,    -- Numeric (exact, for money)
    stock       INTEGER NOT NULL DEFAULT 0,-- Numeric
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- Date/Time
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP   -- Date/Time
);
```

Every single column from Lesson 2.2 maps cleanly onto one of the 5 groups
above.

## Step 4 — Important reminder: types differ by database engine

Back in [Lesson 2.1](01-what-is-sql.md), we said SQL "transfers" across
PostgreSQL, MySQL, SQL Server, and Oracle. That's true for the *core language*
— but **exact data type names are not identical** across engines. The same
concept often has a different name:

| Concept | PostgreSQL | MySQL | SQL Server | Oracle |
|---|---|---|---|---|
| Auto-incrementing ID | `SERIAL` | `AUTO_INCREMENT` | `IDENTITY` | `sequence` + trigger |
| Arbitrary-length text | `TEXT` | `TEXT` | `VARCHAR(MAX)` | `CLOB` |
| True/false | `BOOLEAN` | `TINYINT(1)` | `BIT` | `NUMBER(1)` |
| Date + time | `TIMESTAMP` | `DATETIME` | `DATETIME2` | `TIMESTAMP` |
| Exact decimal | `DECIMAL(p,s)` | `DECIMAL(p,s)` | `DECIMAL(p,s)` | `NUMBER(p,s)` |

**Why this matters**: if you write `CREATE TABLE` code for PostgreSQL and try
to run it unchanged on MySQL or SQL Server, it can fail or silently behave
differently — `BOOLEAN` isn't real in MySQL the way it is in PostgreSQL, for
example (MySQL treats it as `TINYINT(1)` under the hood). The *skill* of
writing SQL transfers easily; the *exact syntax*, especially around data
types, needs a quick check whenever you switch engines.

## Step 5 — Recap

- A data type controls what's allowed, how it's stored, and what operations work.
- PostgreSQL groups types into: Numeric, Text, Boolean, Date/Time, and
  PostgreSQL-Special (`JSONB`, `UUID`, `ARRAY`, `ENUM`).
- The same concept can have a different name on a different engine — always
  check the specific engine's docs when switching.

---
← [2.3 Types of SQL Queries](03-types-of-sql-queries.md)
