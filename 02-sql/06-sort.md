← [2.5 Operators](05-operators.md)

# 2.6 Sort

Now that you can filter rows with [Operators](05-operators.md), let's control
the **order** they come back in — and how to grab just a slice of them.

## Step 0 — Same data as before

Continuing with our `products` table exactly as it stood in
[Lesson 2.5](05-operators.md):

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

## Step 1 — `ORDER BY` (sorting)

```sql
SELECT name, price FROM products ORDER BY price ASC;
```
| name | price |
|---|---|
| AirPods Max | 549.00 |
| iPad Air | 599.00 |
| Mac Mini | 599.00 |
| MacBook Air | 989.10 |
| iPad Pro | 999.00 |
| iPhone 17 | 999.00 |
| iPhone 17 Pro | 1249.00 |
| MacBook Pro | 1799.10 |

`ASC` (ascending, smallest first) is the default — you can leave it off.
`DESC` reverses it:

```sql
SELECT name, price FROM products ORDER BY price DESC;
```
Same rows, largest price first.

## Step 2 — Rows can tie — sort by more than one column

Notice `iPad Air` / `Mac Mini` (both 599.00) and `iPad Pro` / `iPhone 17`
(both 999.00) are **tied** in Step 1 — PostgreSQL doesn't guarantee which
comes first within a tie unless you tell it. Fix that by sorting on a second
column:

```sql
SELECT name, category, price FROM products ORDER BY category ASC, price DESC;
```
| name | category | price |
|---|---|---|
| AirPods Max | audio | 549.00 |
| Mac Mini | desktop | 599.00 |
| MacBook Pro | laptop | 1799.10 |
| MacBook Air | laptop | 989.10 |
| iPhone 17 Pro | smartphone | 1249.00 |
| iPhone 17 | smartphone | 999.00 |
| iPad Pro | tablet | 999.00 |
| iPad Air | tablet | 599.00 |

Read this as: *"group by category alphabetically, and within each category,
show the most expensive first."*

## Step 3 — `LIMIT` and `OFFSET` (paging results)

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 3;
```
| name | price |
|---|---|
| MacBook Pro | 1799.10 |
| iPhone 17 Pro | 1249.00 |
| iPad Pro | 999.00 |

That last row is another tie (iPad Pro vs. iPhone 17, both 999.00) — exactly
why real applications usually add `, product_id` as a tiebreaker in `ORDER BY`
whenever `LIMIT` is involved, so "the top 3" is always the same 3 rows:

```sql
SELECT name, price FROM products ORDER BY price DESC, product_id ASC LIMIT 3;
```

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 3 OFFSET 3;
```
Skips the first 3 results and returns the next 3 — this is how "page 2" of a
paginated list works.

## Step 4 — Putting `WHERE` and `ORDER BY` together

```sql
SELECT name, category, price
FROM products
WHERE category <> 'smartphone'
ORDER BY price ASC
LIMIT 3;
```
| name | category | price |
|---|---|---|
| AirPods Max | audio | 549.00 |
| iPad Air | tablet | 599.00 |
| Mac Mini | desktop | 599.00 |

Read top to bottom: *"take every non-smartphone product, sort cheapest
first, and show me just the top 3."* This is the logical order PostgreSQL
actually processes a query in, even though you type `SELECT` first:

```mermaid
flowchart LR
    A[FROM products] --> B[WHERE category <> 'smartphone']
    B --> C[ORDER BY price ASC]
    C --> D[LIMIT 3]
    D --> E[SELECT name, category, price]
```

## Step 5 — Recap

| Clause | Purpose | Example |
|---|---|---|
| `ORDER BY ... ASC/DESC` | Sort results | `ORDER BY price DESC` |
| Multi-column `ORDER BY` | Break ties deterministically | `ORDER BY category ASC, price DESC` |
| `LIMIT` | Take only the first N rows | `LIMIT 3` |
| `OFFSET` | Skip the first N rows (paging) | `LIMIT 3 OFFSET 3` |

---
← [2.5 Operators](05-operators.md) | Next: [2.7 Functions →](07-functions.md)
