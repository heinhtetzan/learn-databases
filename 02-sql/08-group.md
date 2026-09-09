← [2.7 Functions](07-functions.md)

# 2.8 Group

[Lesson 2.7](07-functions.md) used `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` to
collapse the **entire** `products` table into one summary row. `GROUP BY`
gets you one summary row **per category** instead — the same functions,
bucketed.

## Step 0 — Same data as before

| product_id | name | category | price | stock |
|---|---|---|---|---|
| 1 | iPhone 17 Pro | smartphone | 1249.00 | 500 |
| 2 | MacBook Air | laptop | 989.10 | 300 |
| 3 | MacBook Pro | laptop | 1799.10 | 200 |
| 4 | iPad Air | tablet | 599.00 | 400 |
| 5 | iPad Pro | tablet | 999.00 | 350 |
| 7 | AirPods Max | audio | 549.00 | 250 |
| 10 | Mac Mini | desktop | 599.00 | 450 |
| 11 | iPhone 17 | smartphone | 999.00 | 600 |

## Step 1 — Why `GROUP BY`

Question: *"how many products do we have in each category?"* Without
`GROUP BY`, you'd have to run `SELECT * FROM products`, then count by eye,
category by category. `GROUP BY` does this in one statement:

```sql
SELECT category, COUNT(*) AS num_products
FROM products
GROUP BY category;
```
| category | num_products |
|---|---|
| smartphone | 2 |
| laptop | 2 |
| tablet | 2 |
| audio | 1 |
| desktop | 1 |

`GROUP BY category` collapses all rows sharing the same `category` value into
one row, and `COUNT(*)` — from [Lesson 2.7](07-functions.md) — counts how many
original rows fed into each group.

## Step 2 — The same aggregate functions, now per group

```sql
SELECT category, SUM(price) AS total_value, AVG(price) AS avg_price
FROM products
GROUP BY category;
```
| category | total_value | avg_price |
|---|---|---|
| smartphone | 2248.00 | 1124.00 |
| laptop | 2788.20 | 1394.10 |
| tablet | 1598.00 | 799.00 |
| audio | 549.00 | 549.00 |
| desktop | 599.00 | 599.00 |

`SUM` adds up every `price` in the group; `AVG` divides that sum by the
group's row count. For `audio` and `desktop` — each with only 1 row — the sum
and average are naturally the same number.

```sql
SELECT category, MIN(price) AS cheapest, MAX(price) AS priciest
FROM products
GROUP BY category;
```
| category | cheapest | priciest |
|---|---|---|
| smartphone | 999.00 | 1249.00 |
| laptop | 989.10 | 1799.10 |
| tablet | 599.00 | 999.00 |
| audio | 549.00 | 549.00 |
| desktop | 599.00 | 599.00 |

## Step 3 — The rule: every non-aggregated column must be in `GROUP BY`

```sql
-- ❌ Error: "product_id" is neither grouped nor aggregated
SELECT category, product_id, COUNT(*) FROM products GROUP BY category;
```

PostgreSQL can't decide *which* `product_id` to show for a group containing
multiple rows — so it refuses. Every column in `SELECT` must either be:
1. Listed in `GROUP BY`, or
2. Wrapped in an aggregate function ([Lesson 2.7](07-functions.md)'s
   `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).

## Step 4 — `HAVING`: filtering *groups*, not rows

`WHERE` filters individual rows **before** grouping happens. `HAVING` filters
**groups**, after they've been formed — and it's the only place you're
allowed to filter by an aggregate result:

```sql
SELECT category, COUNT(*) AS num_products
FROM products
GROUP BY category
HAVING COUNT(*) > 1;
```
| category | num_products |
|---|---|
| smartphone | 2 |
| laptop | 2 |
| tablet | 2 |

`audio` and `desktop` (1 product each) are filtered out — `HAVING` kept only
categories with more than one product. You **cannot** write
`WHERE COUNT(*) > 1` — `WHERE` runs before grouping even exists yet, so it has
no groups to check a count against.

## Step 5 — `WHERE` and `HAVING` together

```sql
SELECT category, AVG(price) AS avg_price
FROM products
WHERE stock > 300
GROUP BY category
HAVING AVG(price) > 700;
```
| category | avg_price |
|---|---|
| smartphone | 1124.00 |
| tablet | 799.00 |

Walk through it in order:
1. **`WHERE stock > 300`** removes individual rows first: MacBook Air (300 —
   not *greater than* 300), MacBook Pro (200), and AirPods Max (250) are all
   dropped. That leaves iPhone 17 Pro, iPad Air, iPad Pro, Mac Mini, and
   iPhone 17.
2. **`GROUP BY category`** buckets what's left: `smartphone` (iPhone 17 Pro,
   iPhone 17), `tablet` (iPad Air, iPad Pro), `desktop` (Mac Mini). Notice
   `laptop` and `audio` have **no rows left at all** — every one of their rows
   got filtered out in step 1, so those groups don't exist anymore, not even
   with a zero.
3. **`HAVING AVG(price) > 700`** checks each remaining group's average:
   `smartphone` = 1124.00 ✅, `tablet` = 799.00 ✅, `desktop` = 599.00 ❌ — so
   `desktop` is the one dropped here, leaving exactly the 2 rows shown above.

## Step 6 — The full logical order

```mermaid
flowchart LR
    A[FROM products] --> B[WHERE: filter rows]
    B --> C[GROUP BY: bucket rows]
    C --> D[HAVING: filter groups]
    D --> E[ORDER BY / LIMIT]
    E --> F[SELECT: choose columns]
```

`WHERE` only ever sees individual rows; `HAVING` only ever sees already-formed
groups. Mixing up which one you need is the most common `GROUP BY` mistake —
if your condition uses an aggregate function from
[Lesson 2.7](07-functions.md), it belongs in `HAVING`, never `WHERE`.

## Step 7 — Recap

| Clause | Filters | Can use aggregate functions? |
|---|---|---|
| `WHERE` | Individual rows, before grouping | No |
| `GROUP BY` | (buckets rows, doesn't filter) | — |
| `HAVING` | Groups, after grouping | Yes |

That wraps up the core query-building toolkit: operators to filter, `ORDER
BY`/`LIMIT` to sort and page, functions to reshape and summarize values, and
`GROUP BY`/`HAVING` to summarize per category.

---
← [2.7 Functions](07-functions.md)
