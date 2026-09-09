← [2.4 Data Types in PostgreSQL](04-postgresql-data-types.md)

# 2.5 Operators

Every query so far has either grabbed *everything* or matched one exact row.
Now let's properly filter — the thing you'll do in almost every query you
ever write.

## Step 0 — Where our data stands right now

After every insert/update/delete from [Lesson 2.2](02-your-first-database-apple-example.md),
here's what `SELECT * FROM products;` actually returns:

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

(IDs 6, 8, 9 are gone — those were the rows we deleted.) Every example below
runs against exactly this data, so you can check every result by eye.

## Step 1 — `WHERE` with comparison operators

```sql
SELECT name, price FROM products WHERE category = 'tablet';
```
| name | price |
|---|---|
| iPad Air | 599.00 |
| iPad Pro | 999.00 |

```sql
SELECT name, price FROM products WHERE price > 1000;
```
| name | price |
|---|---|
| iPhone 17 Pro | 1249.00 |
| MacBook Pro | 1799.10 |

```sql
SELECT name FROM products WHERE category <> 'smartphone';
```
Returns every row **except** the 2 smartphones (`<>` means "not equal to").

| Operator | Meaning |
|---|---|
| `=` | equal to |
| `<>` or `!=` | not equal to |
| `<` / `<=` | less than / less than or equal |
| `>` / `>=` | greater than / greater than or equal |

## Step 2 — `BETWEEN` (inclusive range)

```sql
SELECT name, price FROM products WHERE price BETWEEN 500 AND 1000;
```
| name | price |
|---|---|
| MacBook Air | 989.10 |
| iPad Air | 599.00 |
| iPad Pro | 999.00 |
| AirPods Max | 549.00 |
| Mac Mini | 599.00 |
| iPhone 17 | 999.00 |

`BETWEEN 500 AND 1000` includes both endpoints — it's shorthand for
`price >= 500 AND price <= 1000`.

## Step 3 — `IN` (match any value in a list)

```sql
SELECT name, category FROM products WHERE category IN ('laptop', 'tablet');
```
| name | category |
|---|---|
| MacBook Air | laptop |
| MacBook Pro | laptop |
| iPad Air | tablet |
| iPad Pro | tablet |

Without `IN`, you'd need `WHERE category = 'laptop' OR category = 'tablet'` —
`IN` is just a cleaner way to write "matches any of these."

## Step 4 — `LIKE` (pattern matching on text)

```sql
SELECT name FROM products WHERE name LIKE 'iPhone%';
```
| name |
|---|
| iPhone 17 Pro |
| iPhone 17 |

```sql
SELECT name FROM products WHERE name LIKE '%Pro%';
```
| name |
|---|
| iPhone 17 Pro |
| MacBook Pro |
| iPad Pro |

`%` matches *any number* of characters. `'iPhone%'` means "starts with
iPhone"; `'%Pro%'` means "contains Pro anywhere."

## Step 5 — `IS NULL` / `IS NOT NULL`

None of our `products` columns allow `NULL` (they're all `NOT NULL`), so
there's nothing to demonstrate on this table. To see it clearly, imagine a
separate `customers` table where `phone` is optional:

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    phone       TEXT          -- allowed to be NULL: not every customer gives one
);

SELECT name FROM customers WHERE phone IS NULL;
```

⚠️ Never write `WHERE phone = NULL` — in SQL, `NULL` means "unknown," and
"unknown equals unknown" is itself unknown, not true. `= NULL` matches
**nothing**, silently. Always use `IS NULL` / `IS NOT NULL`.

## Step 6 — Combining conditions: `AND`, `OR`, `NOT`

```sql
SELECT name, price FROM products WHERE category = 'laptop' AND price < 1000;
```
| name | price |
|---|---|
| MacBook Air | 989.10 |

(MacBook Pro is a laptop too, but its price — 1799.10 — fails the second
condition, so `AND` excludes it.)

```sql
SELECT name FROM products WHERE category = 'tablet' OR category = 'audio';
```
| name |
|---|
| iPad Air |
| iPad Pro |
| AirPods Max |

```sql
SELECT name FROM products WHERE NOT category = 'smartphone';
```
Same result as Step 1's `<>` example — `NOT` negates whatever condition
follows it.

> **Precedence trap**: `AND` binds tighter than `OR`. When mixing them, always
> add parentheses to be explicit:
> `WHERE category = 'laptop' AND (price < 1000 OR stock > 300)`

## Step 7 — Recap

| Operator | Purpose | Example |
|---|---|---|
| `=`, `<>`, `<`, `>`, `<=`, `>=` | Basic comparisons | `WHERE price > 1000` |
| `BETWEEN` | Inclusive range | `WHERE price BETWEEN 500 AND 1000` |
| `IN` | Match any of a list | `WHERE category IN ('laptop','tablet')` |
| `LIKE` | Text pattern match | `WHERE name LIKE 'iPhone%'` |
| `IS NULL` / `IS NOT NULL` | Check for missing values | `WHERE phone IS NULL` |
| `AND` / `OR` / `NOT` | Combine conditions | `WHERE category='laptop' AND price<1000` |

---
← [2.4 Data Types in PostgreSQL](04-postgresql-data-types.md) | Next: [2.6 Sort →](06-sort.md)
