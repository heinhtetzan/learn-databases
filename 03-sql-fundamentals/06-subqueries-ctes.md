← [Module 03](README.md) | [Course Home](../README.md)

# 3.6 Subqueries & CTEs

Sometimes a question naturally breaks into steps: "first find X, then use it to
find Y." Subqueries and CTEs (Common Table Expressions) let you express that
directly in SQL.

## Subqueries in `WHERE`

```sql
-- Books priced above the overall average price
SELECT title, price
FROM books
WHERE price > (SELECT AVG(price) FROM books);
```

The inner query `(SELECT AVG(price) FROM books)` runs first (conceptually),
producing a single value the outer query then compares against.

## `IN` / `NOT IN` with subqueries

```sql
-- Customers who have placed at least one order
SELECT name FROM customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders);

-- Books that have NEVER been ordered
SELECT title FROM books
WHERE book_id NOT IN (SELECT book_id FROM order_items);
```

> ⚠️ **`NOT IN` + `NULL` trap**: if the subquery can return a `NULL` value,
> `NOT IN` silently returns **zero rows** for the entire query — a notorious SQL
> gotcha. Prefer `NOT EXISTS` (below) for this pattern, since it doesn't have
> this issue.

## `EXISTS` / `NOT EXISTS`

`EXISTS` checks only whether the subquery returns *any* row — often faster than
`IN` for large subqueries, and safe with `NULL`s:

```sql
-- Customers who have placed at least one order (EXISTS version)
SELECT name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);

-- Authors with no books at all
SELECT name FROM authors a
WHERE NOT EXISTS (
    SELECT 1 FROM books b WHERE b.author_id = a.author_id
);
```

## Subqueries in `FROM` (derived tables)

Treat a query's result as if it were a table:

```sql
SELECT genre, avg_price
FROM (
    SELECT genre, AVG(price) AS avg_price
    FROM books
    GROUP BY genre
) AS genre_stats
WHERE avg_price > 15;
```

## Correlated subqueries

A subquery that references a column from the *outer* query — it re-runs once
per outer row, conceptually:

```sql
-- Each book's price compared to the average price in its OWN genre
SELECT title, genre, price
FROM books b1
WHERE price > (
    SELECT AVG(price) FROM books b2 WHERE b2.genre = b1.genre
);
```

## CTEs: `WITH ... AS`

A **CTE** names a subquery up front, making complex queries far more readable —
especially once you need the same intermediate result more than once, or want
to build a query in clear, named steps.

```sql
WITH customer_spend AS (
    SELECT c.customer_id, c.name, SUM(oi.quantity * oi.unit_price) AS total_spent
    FROM customers c
    JOIN orders o       ON o.customer_id = c.customer_id
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY c.customer_id, c.name
)
SELECT name, total_spent
FROM customer_spend
WHERE total_spent > 100
ORDER BY total_spent DESC;
```

This is functionally the same as a `FROM`-subquery, but reads top-to-bottom like
a small program: "first compute `customer_spend`, then filter it." You can chain
multiple CTEs:

```sql
WITH genre_avg AS (
    SELECT genre, AVG(price) AS avg_price FROM books GROUP BY genre
),
above_avg_books AS (
    SELECT b.title, b.genre, b.price
    FROM books b
    JOIN genre_avg g ON b.genre = g.genre
    WHERE b.price > g.avg_price
)
SELECT * FROM above_avg_books ORDER BY genre, price DESC;
```

## Recursive CTEs (a preview)

CTEs can reference *themselves*, which is how SQL handles hierarchical/recursive
data (org charts, category trees, graph traversal) without a client-side loop:

```sql
WITH RECURSIVE org_chart AS (
    SELECT employee_id, name, manager_id, 1 AS depth
    FROM employees WHERE manager_id IS NULL          -- anchor: the top of the org
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id, oc.depth + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id  -- recursive step
)
SELECT * FROM org_chart ORDER BY depth;
```

Advanced, but worth recognizing — it's the standard SQL answer to "give me this
whole tree/hierarchy in one query."

## Subquery vs. join vs. CTE — how to choose

| Use | When |
|---|---|
| **Join** | You need columns from both tables side-by-side in the result |
| **Subquery in `WHERE`/`EXISTS`** | You only need to *filter* based on another table, not display its columns |
| **CTE** | The query has multiple logical steps, or you reuse the same intermediate result more than once — pure readability tool, usually no different from a subquery to the query planner |

## Try it yourself

Using the bookstore schema:
1. Find all books priced above the average price *of their own genre*
   (correlated subquery).
2. Rewrite it as a CTE (`genre_avg` computed once, then joined).
3. Find every customer who has placed **zero** orders, using `NOT EXISTS`.
4. Using a CTE, compute each customer's total spend, then select only customers
   whose spend is above the overall average spend across all customers (a CTE
   feeding into another calculation — two logical steps).

---
← [3.5 Aggregation & Grouping](05-aggregation-grouping.md) | [Module 03](README.md) | Next: [Module 04 — Schema Design →](../04-schema-design/)
