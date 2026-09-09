← [Module 03](README.md) | [Course Home](../README.md)

# 3.3 Filtering & Sorting

This lesson covers narrowing down and ordering results — the two things you'll
do in almost every query you ever write.

## `WHERE`: filtering rows

```sql
SELECT title, price FROM books WHERE genre = 'Science Fiction';
SELECT title FROM books WHERE price > 15;
SELECT title FROM books WHERE price BETWEEN 10 AND 20;
SELECT title FROM books WHERE genre IN ('Science Fiction', 'Fantasy');
SELECT title FROM books WHERE title LIKE 'The%';       -- starts with "The"
SELECT * FROM books WHERE stock = 0;
SELECT * FROM authors WHERE country IS NULL;           -- never use = NULL, it never matches
```

### Comparison and logical operators

| Operator | Meaning |
|---|---|
| `=`, `<>` / `!=` | equals, not equals |
| `<`, `<=`, `>`, `>=` | less/greater than (or equal) |
| `BETWEEN a AND b` | inclusive range |
| `IN (...)` | matches any value in a list |
| `LIKE` / `ILIKE` (Postgres, case-insensitive) | pattern match (`%` = any characters, `_` = one character) |
| `IS NULL` / `IS NOT NULL` | null checks (never use `=` or `<>` with `NULL`) |
| `AND`, `OR`, `NOT` | combine conditions |

```sql
SELECT title, price, stock
FROM books
WHERE genre = 'Fantasy'
  AND price < 20
  AND stock > 0;

SELECT title FROM books
WHERE NOT (genre = 'Fantasy' OR genre = 'Science Fiction');
```

> **Operator precedence trap**: `AND` binds tighter than `OR`. Always
> parenthesize when mixing them:
> `WHERE genre = 'Fantasy' AND (price < 10 OR stock = 0)`

## `ORDER BY`: sorting results

```sql
SELECT title, price FROM books ORDER BY price;             -- ascending (default)
SELECT title, price FROM books ORDER BY price DESC;         -- descending
SELECT title, genre, price FROM books
ORDER BY genre ASC, price DESC;                              -- multi-column sort
```

Rows have **no guaranteed order** unless you specify `ORDER BY` — never rely on
"the order rows happen to come back in."

## `LIMIT` / `OFFSET`: paging results

```sql
SELECT title, price FROM books ORDER BY price DESC LIMIT 5;             -- top 5 most expensive
SELECT title, price FROM books ORDER BY price DESC LIMIT 5 OFFSET 5;    -- next 5 ("page 2")
```

> **`OFFSET` doesn't scale well** — `OFFSET 1000000` still has to scan and
> discard a million rows internally. For large paginated datasets, "keyset
> pagination" (filtering by `WHERE id > <last_seen_id>` instead of `OFFSET`) is
> far more efficient — worth knowing exists once you hit real scale, covered
> briefly in [Module 05, Lesson 3](../05-indexing-performance/03-performance-tuning.md).

## `DISTINCT`: removing duplicates

```sql
SELECT DISTINCT genre FROM books;                 -- every unique genre, once each
SELECT DISTINCT city FROM customers;
```

## Combining it all

```sql
SELECT title, genre, price
FROM books
WHERE genre IN ('Fantasy', 'Science Fiction')
  AND stock > 0
ORDER BY price DESC
LIMIT 3;
```

Logical order SQL executes conceptually (not the order you *type* it in):

```mermaid
flowchart LR
    A[FROM / JOIN] --> B[WHERE]
    B --> C[GROUP BY]
    C --> D[HAVING]
    D --> E[SELECT]
    E --> F[ORDER BY]
    F --> G[LIMIT / OFFSET]
```

This explains some SQL quirks: you *can't* reference a `SELECT`-defined alias in
`WHERE` (because `WHERE` runs before `SELECT` conceptually), but you *can* use
one in `ORDER BY` (which runs after). `GROUP BY`/`HAVING` are covered in
[Lesson 5](05-aggregation-grouping.md).

## Try it yourself

Using the bookstore schema:
1. Find all books priced between $10 and $20, sorted cheapest first.
2. Find all books whose title contains the word "the" (case-insensitive).
3. List the 3 most expensive books currently in stock (`stock > 0`).
4. List every distinct city your customers live in.

---
← [3.2 DML & CRUD](02-dml-crud.md) | [Module 03](README.md) | Next: [Joins →](04-joins.md)
