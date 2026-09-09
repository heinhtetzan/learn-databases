← [2.6 Sort](06-sort.md)

# 2.7 Functions

A **function** takes some input and computes an output — SQL has built-in
functions for aggregating, reshaping text, doing math, and working with
dates. Let's meet the core ones before putting the most important group —
aggregate functions — to real use in the next lesson.

## Step 1 — Aggregate functions

These summarize *many* rows down into **one** value:

```sql
SELECT COUNT(*) FROM products;
```
| count |
|---|
| 8 |

```sql
SELECT SUM(stock) AS total_stock, AVG(price) AS avg_price FROM products;
```
| total_stock | avg_price |
|---|---|
| 3050 | 972.775000 |

```sql
SELECT MIN(price) AS cheapest, MAX(price) AS priciest FROM products;
```
| cheapest | priciest |
|---|---|
| 549.00 | 1799.10 |

| Function | Does |
|---|---|
| `COUNT(*)` | Number of rows |
| `SUM(column)` | Total of a numeric column |
| `AVG(column)` | Average of a numeric column |
| `MIN(column)` / `MAX(column)` | Smallest / largest value |

Used like this, each one collapses the **entire table** into a single
summary row. [Lesson 2.8 — Group](08-group.md) shows how to get one summary
row *per category* instead, using these exact same functions.

Notice `avg_price` came back with extra decimal digits — PostgreSQL doesn't
round it for you automatically. That's exactly what the next section fixes.

## Step 2 — Math functions

```sql
SELECT ROUND(AVG(price), 2) AS avg_price FROM products;
```
| avg_price |
|---|
| 972.78 |

`ROUND(value, decimal_places)` rounds to however many decimal places you ask
for.

```sql
SELECT name, price, ROUND(price) AS rounded, CEIL(price) AS rounded_up, FLOOR(price) AS rounded_down
FROM products WHERE product_id = 2;
```
| name | price | rounded | rounded_up | rounded_down |
|---|---|---|---|---|
| MacBook Air | 989.10 | 989 | 990 | 989 |

- `ROUND` — nearest whole number (or nearest N decimal places, if given a second argument)
- `CEIL` — always rounds **up**
- `FLOOR` — always rounds **down**
- `ABS` — absolute value: `SELECT ABS(-42);` → `42`

## Step 3 — String functions

```sql
SELECT UPPER(name) FROM products WHERE product_id = 1;
```
→ `IPHONE 17 PRO`

```sql
SELECT LOWER(name) FROM products WHERE product_id = 2;
```
→ `macbook air`

```sql
SELECT name, LENGTH(name) FROM products WHERE product_id = 1;
```
| name | length |
|---|---|
| iPhone 17 Pro | 13 |

```sql
SELECT name || ' (' || category || ')' AS label FROM products WHERE product_id = 1;
```
→ `iPhone 17 Pro (smartphone)`

`||` glues text together (PostgreSQL's concatenation operator) — `CONCAT(name, ' (', category, ')')` does the same thing as a function call instead.

```sql
SELECT SUBSTRING(name FROM 1 FOR 3) FROM products WHERE product_id = 2;
```
→ `Mac` — takes 3 characters starting from position 1.

```sql
SELECT TRIM('  hello  ');
```
→ `hello` — strips leading/trailing whitespace.

## Step 4 — Date/time functions

```sql
SELECT CURRENT_DATE;
```
→ today's date, whatever day you actually run it (e.g., `2026-09-09`).

```sql
SELECT EXTRACT(YEAR FROM created_at) AS year FROM products WHERE product_id = 1;
```
If `created_at` is `2026-02-01 ...`, this returns `2026`. `EXTRACT` pulls out
one specific part (`YEAR`, `MONTH`, `DAY`, `HOUR`, ...) from a date/time value.

```sql
SELECT AGE(CURRENT_DATE, created_at) FROM products WHERE product_id = 1;
```
If `created_at` was `2026-02-01` and today is `2026-09-09`, this returns an
interval like `7 mons 8 days` — `AGE` computes the human-readable span between
two dates, exactly the kind of thing you'd use for "member since 7 months
ago."

## Step 5 — `COALESCE`: a default value for `NULL`

Back in [Lesson 2.5](05-operators.md) we used a `customers` table where
`phone` could be `NULL`. `COALESCE` lets you substitute a fallback value
whenever a column is `NULL`:

```sql
SELECT name, COALESCE(phone, 'no phone provided') AS phone
FROM customers;
```
Any customer with a real phone number shows it; any customer with `NULL`
shows `'no phone provided'` instead. `COALESCE` checks its arguments in order
and returns the first one that isn't `NULL`.

## Step 6 — Recap

| Category | Functions | Example |
|---|---|---|
| Aggregate | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | `SELECT AVG(price) FROM products;` |
| Math | `ROUND`, `CEIL`, `FLOOR`, `ABS` | `ROUND(price, 2)` |
| String | `UPPER`, `LOWER`, `LENGTH`, `\|\|`/`CONCAT`, `SUBSTRING`, `TRIM` | `name \|\| ' (' \|\| category \|\| ')'` |
| Date/Time | `CURRENT_DATE`, `EXTRACT`, `AGE` | `EXTRACT(YEAR FROM created_at)` |
| Null handling | `COALESCE` | `COALESCE(phone, 'no phone provided')` |

Aggregate functions are the ones to hold onto tightly — the next lesson
builds directly on them.

---
← [2.6 Sort](06-sort.md) | Next: [2.8 Group →](08-group.md)
