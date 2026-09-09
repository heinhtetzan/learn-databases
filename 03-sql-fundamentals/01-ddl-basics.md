← [Module 03](README.md) | [Course Home](../README.md)

# 3.1 DDL Basics

**DDL (Data Definition Language)** is the subset of SQL that defines and modifies
*structure* — tables, columns, constraints, indexes — as opposed to **DML** (Data
Manipulation Language), which reads and writes the *data itself* (next lesson).

## `CREATE TABLE`

```sql
CREATE TABLE authors (
    author_id   INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    country     TEXT
);
```

Every column declares a **data type**. Common types across most SQL databases:

| Category | Types | Notes |
|---|---|---|
| Integer | `INTEGER`, `SMALLINT`, `BIGINT` | Whole numbers; pick size based on expected range |
| Decimal | `DECIMAL(p,s)` / `NUMERIC(p,s)` | Exact precision — **always use for money**, never `FLOAT` |
| Floating point | `REAL`, `FLOAT`, `DOUBLE` | Approximate — fine for scientific data, risky for money |
| Text | `TEXT`, `VARCHAR(n)`, `CHAR(n)` | `VARCHAR(n)` caps length; `TEXT` is usually unlimited |
| Boolean | `BOOLEAN` | True/false |
| Date/Time | `DATE`, `TIME`, `TIMESTAMP` | Store timestamps in UTC; convert for display |
| Binary | `BYTEA` (Postgres), `BLOB` (MySQL/SQLite) | Raw binary data — usually better stored outside the DB with a reference |
| Structured | `JSON` / `JSONB` (Postgres) | Semi-structured data inside a relational table (see [Module 07](../07-nosql/01-nosql-overview.md) for when to lean on this more heavily) |

> **Why `DECIMAL` for money, never `FLOAT`?** Floating-point numbers can't
> represent most decimal fractions exactly (`0.1 + 0.2` famously isn't quite `0.3`
> in floating point). `DECIMAL(10,2)` stores exact digits — essential once real
> money is involved.

## `ALTER TABLE`

Modify an existing table's structure without recreating it:

```sql
ALTER TABLE books ADD COLUMN language TEXT DEFAULT 'en';
ALTER TABLE books ALTER COLUMN price SET NOT NULL;
ALTER TABLE books DROP COLUMN language;
ALTER TABLE books RENAME COLUMN genre TO category;
```

> **Caution**: `ALTER TABLE` on a huge production table can lock it for reads/
> writes while it runs, depending on the database and the specific change.
> We cover safe migration strategies briefly in
> [Module 09](../09-security-and-administration/02-backup-recovery.md).

## `DROP TABLE` and `TRUNCATE TABLE`

```sql
DROP TABLE books;        -- deletes the table AND all its data, structure gone
TRUNCATE TABLE books;    -- deletes all rows, keeps the table structure
```

Both are effectively irreversible outside of a transaction or backup — never run
either against production without a very good reason and a backup.

## Indexes (a first look)

```sql
CREATE INDEX idx_books_author ON books(author_id);
```

This tells the DBMS to maintain a fast lookup structure on `author_id`, so
queries filtering or joining on it don't need to scan the whole table. We
dedicate all of [Module 05](../05-indexing-performance/01-indexes-explained.md) to
how these work internally and when to add them.

## Schemas/namespaces (brief mention)

Most production databases group tables into named **schemas** (Postgres) or
**databases** (MySQL) for organization and permissions:

```sql
CREATE SCHEMA bookstore;
CREATE TABLE bookstore.books (...);
```

You won't need this for the exercises in this course, but expect to see
`schema.table` naming in real codebases.

## Try it yourself

1. Run the full bookstore schema from the [module README](README.md) setup section.
2. Add a `language` column to `books`, defaulting to `'en'`, then remove it again.
3. Add a `CHECK` constraint to `customers` ensuring `email` contains an `@`
   character (hint: `CHECK (email LIKE '%@%')`).

---
← [Module 03](README.md) | Next: [DML & CRUD →](02-dml-crud.md)
