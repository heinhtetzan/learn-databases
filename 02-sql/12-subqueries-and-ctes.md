← [2.11 Joins](11-joins.md)

# 2.12 Subqueries & CTEs

Before any syntax, 3 real-world questions that naturally break into steps.

## 3 real-world scenarios

**1. A shop** asks *"which products are priced above our own average
price?"* — you can't answer that in one glance; you first need the average
computed, then compare every product against it.

**2. A university** wants *"students with no failing grades"* — that means
checking each student against a whole separate table of grades, not
comparing against one fixed value.

**3. A hospital** builds a report in two steps: first compute each doctor's
current patient count, then filter down to only the doctors above a certain
caseload — the second step depends entirely on the first being computed
already.

## Why subqueries and CTEs

Each scenario needs an intermediate result — an average, a check against
another table, a computed count — used *inside* a bigger query. Subqueries
and CTEs let you write that directly in SQL: *"first find X, then use it to
find Y."* Every example below uses the same
`customers`/`orders`/`order_items`/`products` schema from
[Lesson 2.10](10-relationships-and-foreign-keys.md).

## Step 1 — A subquery in `WHERE`

```sql
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```
| name | price |
|---|---|
| iPhone 17 Pro | 1249.00 |
| MacBook Air | 989.10 |
| MacBook Pro | 1799.10 |
| iPad Pro | 999.00 |
| iPhone 17 | 999.00 |

The inner query `(SELECT AVG(price) FROM products)` runs first, producing one
number (972.775 — from [Lesson 2.7](07-functions.md)'s recap of `AVG`), which
the outer query then compares every row's `price` against.

## Step 2 — `IN` with a subquery

```sql
SELECT name FROM customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders);
```
| name |
|---|
| Alice Chen |
| Bob Diaz |

Carla is excluded — her `customer_id` never appears in `orders`.

## Step 3 — The `NOT IN` trap, and the safer fix

```sql
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```
| name |
|---|
| Carla Ruiz |

This works correctly here — but only because `orders.customer_id` is
`NOT NULL` ([Lesson 2.10](10-relationships-and-foreign-keys.md)'s foreign
key). **If that subquery could ever return even one `NULL`, `NOT IN` would
silently return zero rows for the entire query** — a notorious, easy-to-miss
SQL bug. The safer habit, which works regardless:

```sql
SELECT name FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```
Same result — `EXISTS` only checks *whether any row matches*, so `NULL`s in
the subquery can't break it.

## Step 4 — `EXISTS`, the positive version

```sql
SELECT name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```
| name |
|---|
| Alice Chen |
| Bob Diaz |

## Step 5 — A subquery in `FROM` (a "derived table")

Treat a query's result as if it were its own table:

```sql
SELECT category, avg_price
FROM (
    SELECT category, AVG(price) AS avg_price
    FROM products
    GROUP BY category
) AS category_stats
WHERE avg_price > 700;
```
| category | avg_price |
|---|---|
| smartphone | 1124.00 |
| laptop | 1394.10 |
| tablet | 799.00 |

(`audio` at 549.00 and `desktop` at 599.00 — from
[Lesson 2.8](08-group.md)'s `GROUP BY` results — don't clear 700, so they're
filtered out.)

## Step 6 — The same query, as a CTE

A **CTE** (`WITH ... AS`) names a subquery up front, so a query reads
top-to-bottom like a small program instead of nesting nested parentheses:

```sql
WITH category_stats AS (
    SELECT category, AVG(price) AS avg_price
    FROM products
    GROUP BY category
)
SELECT category, avg_price
FROM category_stats
WHERE avg_price > 700;
```

Identical result to Step 5 — a CTE is usually just a more readable way to
write the same thing, especially once you need the same intermediate result
more than once in one query.

## Step 7 — A correlated subquery

A subquery that references a column from the *outer* query — it effectively
re-runs once per outer row:

```sql
SELECT name, category, price
FROM products p1
WHERE price > (
    SELECT AVG(price) FROM products p2 WHERE p2.category = p1.category
);
```
| name | category | price |
|---|---|---|
| iPhone 17 Pro | smartphone | 1249.00 |
| MacBook Pro | laptop | 1799.10 |
| iPad Pro | tablet | 999.00 |

This finds products priced above the average **of their own category** —
different from Step 1, which compared against the average of *all* products
combined. iPhone 17 (999.00) doesn't qualify here, even though it beat the
*overall* average in Step 1 — it's below its own category's average (1124.00).

## Step 8 — Recap

| Tool | Use it when |
|---|---|
| Subquery in `WHERE` | You need to filter using a single computed value |
| `IN` / subquery | Match against a list produced by another query |
| `EXISTS` / `NOT EXISTS` | Check for *any* match, safely — even with `NULL`s involved |
| Subquery in `FROM` | You need to query the *result* of another query |
| CTE (`WITH`) | Same as a `FROM`-subquery, but far more readable for multi-step logic |
| Correlated subquery | The inner query depends on each row of the outer query |

---
← [2.11 Joins](11-joins.md) | Next: [2.13 Constraints →](13-constraints.md)
