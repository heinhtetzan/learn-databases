← [2.10 Relationships & Foreign Keys](10-relationships-and-foreign-keys.md)

# 2.11 Joins

This is the single most important skill for querying real, related data.
Before any code, 3 real-world situations where you'd need one.

## 3 real-world scenarios

**1. A shop** keeps a `customers` table (name, email) and a separate `orders`
table (what was bought, when). Neither table alone can answer *"what has
Alice ordered?"* — `customers` doesn't know about orders, and `orders` only
knows a customer *ID*, not a name. You need her row from `customers` **and**
her rows from `orders`, matched together, to answer that.

**2. A university** keeps a `students` table and a `courses` table, connected
through an `enrollments` table (which student is in which course). To answer
*"who is enrolled in Database 101?"*, you need all three — students and
courses never touch each other directly; the enrollment table is the bridge
between them.

**3. A hospital** keeps a `patients` table, a `doctors` table, and an
`appointments` table linking the two. To answer *"which patients does
Dr. Smith see this week?"*, you need `appointments` matched to `doctors` (to
find which appointments belong to Dr. Smith) and to `patients` (to get their
names) — three tables, each holding one piece of a question that spans all
of them.

## What a join actually is

Given those 3 scenarios: a **join** combines rows from two (or more) tables
into one result, matched by a shared piece of information — usually an ID
that one table stores as a foreign key pointing at another (exactly what
[Lesson 2.10](10-relationships-and-foreign-keys.md) set up). In scenario 1,
that shared ID is the customer ID sitting on every order; in scenario 3, it's
the doctor ID and patient ID sitting on every appointment.

## Why joins exist at all

[Lesson 2.9](09-normalization.md) split one messy table into several clean
ones specifically to stop repeating the same information everywhere. But that
means the *pieces* of any real answer — like all 3 scenarios above — now live
in different tables. A join is simply how you put those pieces back together
for one specific question, without undoing the normalization that keeps the
data clean.

## Now, the same idea in SQL

Every example below runs against the exact schema and data from
[Lesson 2.10](10-relationships-and-foreign-keys.md) — our own version of the
"shop" scenario above: `customers`, `orders`, `order_items`, and `products`.

## Step 0 — The data we're working with

**`customers`**: 1=Alice Chen, 2=Bob Diaz, 3=Carla Ruiz (Carla has **no orders**).
**`orders`**: 1 (Alice, 2026-03-01), 2 (Bob, 2026-03-02), 3 (Alice, 2026-03-05).
**`order_items`**: order 1 → products 1 & 7; order 2 → product 2; order 3 → products 5 & 10.

## Step 1 — `INNER JOIN`: only matching rows

```sql
SELECT o.order_id, c.name, o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```
| order_id | name | order_date |
|---|---|---|
| 1 | Alice Chen | 2026-03-01 |
| 2 | Bob Diaz | 2026-03-02 |
| 3 | Alice Chen | 2026-03-05 |

Every order has a matching customer, so nothing is excluded here — but notice
**Carla never appears at all**, since she has no orders to join against.

## Step 2 — `LEFT JOIN`: every row from the left table, matched or not

```sql
SELECT c.name, o.order_id, o.order_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;
```
| name | order_id | order_date |
|---|---|---|
| Alice Chen | 1 | 2026-03-01 |
| Alice Chen | 3 | 2026-03-05 |
| Bob Diaz | 2 | 2026-03-02 |
| Carla Ruiz | `NULL` | `NULL` |

`LEFT JOIN` keeps **every** row from `customers` (the "left" table), filling
in `NULL` where there's no matching order. Carla shows up now, with `NULL`s.

**The single most useful trick this enables**: find every customer with
**zero** orders, by filtering for that `NULL`:

```sql
SELECT c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```
| name |
|---|
| Carla Ruiz |

## Step 3 — `RIGHT JOIN`: the mirror image

```sql
SELECT c.name, o.order_id
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;
```
Identical result to Step 2's `LEFT JOIN` — `RIGHT JOIN` just keeps every row
from whichever table is on the *right*. In practice, most people just reorder
the tables and use `LEFT JOIN` instead, since it reads more naturally
left-to-right — `RIGHT JOIN` is rare to see in real code.

## Step 4 — `FULL OUTER JOIN`: everything from both sides

Our `orders.customer_id` foreign key ([Lesson 2.10](10-relationships-and-foreign-keys.md))
*guarantees* every order has a real customer — so there's no such thing as an
"orphan order" in this schema, and a `FULL OUTER JOIN` between `customers`
and `orders` would look identical to Step 2's `LEFT JOIN`. `FULL OUTER JOIN`
actually earns its keep when two tables *aren't* linked by a foreign key at
all — e.g., merging two independent lists that only sometimes overlap:

```sql
-- Two unrelated lists — no foreign key connects them
SELECT COALESCE(w.email, s.email) AS email, w.email IS NOT NULL AS on_waitlist, s.email IS NOT NULL AS subscribed
FROM waitlist w
FULL OUTER JOIN subscribers s ON w.email = s.email;
```
This returns every email that's on *either* list, showing `NULL` on
whichever side it's missing from — something `INNER`/`LEFT`/`RIGHT` alone
can't give you at once.

## Step 5 — Joining 3+ tables

```sql
SELECT c.name AS customer, o.order_id, p.name AS product,
       oi.quantity, oi.unit_price, oi.quantity * oi.unit_price AS line_total
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
ORDER BY o.order_id, p.product_id;
```
| customer | order_id | product | quantity | unit_price | line_total |
|---|---|---|---|---|---|
| Alice Chen | 1 | iPhone 17 Pro | 1 | 1249.00 | 1249.00 |
| Alice Chen | 1 | AirPods Max | 1 | 549.00 | 549.00 |
| Bob Diaz | 2 | MacBook Air | 1 | 989.10 | 989.10 |
| Alice Chen | 3 | iPad Pro | 1 | 999.00 | 999.00 |
| Alice Chen | 3 | Mac Mini | 1 | 599.00 | 599.00 |

Chain `JOIN`s one at a time, each pulling in one more table — this reads as
"customers, joined to their orders, joined to each order's line items, joined
to what product each line item actually was."

## Step 6 — Bonus: joins + `GROUP BY` together

Bringing in [Lesson 2.7](07-functions.md)'s `SUM`/`COALESCE` and
[Lesson 2.8](08-group.md)'s `GROUP BY`, here's "total spent per customer,"
including customers who've spent nothing:

```sql
SELECT c.name, COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spent
FROM customers c
LEFT JOIN orders o        ON o.customer_id = c.customer_id
LEFT JOIN order_items oi  ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```
| name | total_spent |
|---|---|
| Alice Chen | 3396.00 |
| Bob Diaz | 989.10 |
| Carla Ruiz | 0.00 |

`LEFT JOIN` keeps Carla in the result even with no orders; without
`COALESCE`, her `SUM` would show as `NULL` instead of `0.00` (`SUM` of zero
rows is `NULL`, not zero — `COALESCE` from [Lesson 2.7](07-functions.md)
substitutes a real value).

## Step 7 — Recap

| Join type | Keeps unmatched left rows? | Keeps unmatched right rows? |
|---|---|---|
| `INNER JOIN` | No | No |
| `LEFT JOIN` | **Yes** | No |
| `RIGHT JOIN` | No | **Yes** |
| `FULL OUTER JOIN` | **Yes** | **Yes** |

Joins are what turn 4 separate, normalized tables back into one meaningful
answer — everything from here builds on being comfortable combining tables
this way.

---
← [2.10 Relationships & Foreign Keys](10-relationships-and-foreign-keys.md) | Next: [2.12 Subqueries & CTEs →](12-subqueries-and-ctes.md)
