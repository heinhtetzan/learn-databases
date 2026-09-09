← [2.14 Transactions](14-transactions.md)

# 2.15 Indexes & Performance

Every query so far has run instantly — our tables have a handful of rows.
Real tables have millions. This lesson is about *why* queries stay fast (or
don't) at that scale.

## Step 1 — The problem: scanning is slow at scale

Without help, finding matching rows means checking **every single row** — a
**sequential scan**. `SELECT * FROM order_items WHERE product_id = 4;` on an
`order_items` table with 10 million rows means up to 10 million comparisons.
An **index** is a separate, sorted structure PostgreSQL maintains specifically
to avoid this.

## Step 2 — What's already indexed, and what isn't

From [Lesson 2.13](13-constraints.md): `PRIMARY KEY` and `UNIQUE` columns are
**automatically** indexed — `products.product_id`, `customers.email`, and
`order_items`'s composite `(order_id, product_id)` key all already have one.

**Foreign key columns are *not* automatically indexed in PostgreSQL** — a
common surprise. `orders.customer_id` and `order_items.product_id` (the
columns we constantly `JOIN` on, back in [Lesson 2.11](11-joins.md)) have no
index yet. Let's add them:

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

## Step 3 — Reading `EXPLAIN`

```sql
EXPLAIN SELECT * FROM order_items WHERE product_id = 4;
```
```
Seq Scan on order_items  (cost=0.00..1.06 rows=1 width=24)
  Filter: (product_id = 4)
```

Notice it's still a **`Seq Scan`**, even though we just added an index! On
our actual table — 5 rows — scanning all of them is already faster than the
overhead of using an index. This is the honest, correct picture: the
PostgreSQL query planner is smart enough to know a sequential scan is
genuinely cheaper here. Indexes start winning once a table has thousands to
millions of rows. On a table that large, the same query's plan would instead
look like:

```
-- Illustrative: same query, on a table with millions of rows
Index Scan using idx_order_items_product_id on order_items  (cost=0.42..8.44 rows=120 width=24)
  Index Cond: (product_id = 4)
```

`Index Scan` means PostgreSQL jumped straight to matching rows via the index,
instead of reading the whole table.

## Step 4 — Composite indexes and column order

```sql
CREATE INDEX idx_products_category_price ON products(category, price);
```

Column order matters. This index efficiently supports:
- `WHERE category = 'laptop'` ✅ (leftmost column alone)
- `WHERE category = 'laptop' AND price > 1000` ✅ (both, in order)

...but **not**:
- `WHERE price > 1000` alone ❌ — the index is sorted by `category` first, so
  without a `category` filter, PostgreSQL can't jump straight to a price
  range.

**Rule of thumb**: put the column you filter with `=` first, range/sort
columns after.

## Step 5 — When an index doesn't help (or actively hurts)

| Situation | Why |
|---|---|
| Small table (our whole database right now) | A sequential scan is already fast; index overhead isn't worth it |
| Low-cardinality column (e.g., a boolean) | The index barely narrows anything down |
| Query returns most of the table anyway | Scanning sequentially can beat jumping around via an index |
| Table is written to far more than read | Every `INSERT`/`UPDATE`/`DELETE` must also update every index on that table |

**Rule of thumb**: index columns you filter, join, or sort on frequently, on
tables that are large and read often. Don't index "just in case."

## Step 6 — Recap

| Concept | Takeaway |
|---|---|
| `PRIMARY KEY` / `UNIQUE` | Already indexed automatically |
| Foreign key columns | **Not** automatically indexed — add manually if you join/filter on them often |
| `EXPLAIN` | Shows the real plan — always check before assuming an index is used |
| Composite index order | Equality columns first, range columns after |
| Small tables | May correctly ignore your index — that's expected, not a bug |

---
← [2.14 Transactions](14-transactions.md) | Next: [2.16 Views →](16-views.md)
