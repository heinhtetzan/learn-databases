← [4.1 The Same Data, Two Ways](01-same-data-two-ways.md)

# 4.2 The Same Query, Two Ways

4 real queries, run against the exact same data in both databases —
straight from Parts 1 and 2.

## Query 1: Filter — laptops under $1000

```sql
-- SQL (Lesson 2.5)
SELECT name, price FROM products WHERE category = 'laptop' AND price < 1000;
```
```js
// MongoDB (Lesson 3.5)
db.products.find({ category: "laptop", price: { $lt: 1000 } });
```
Both return: **MacBook Air, 989.10**. Roughly the same amount of typing,
roughly the same shape of thinking.

## Query 2: Find unmatched rows — customers with zero orders

```sql
-- SQL (Lesson 2.11)
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```
```js
// MongoDB (Lesson 3.11)
db.customers.aggregate([
  { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } },
  { $match: { orders: { $size: 0 } } }
]);
```
Both return: **Carla Ruiz**. SQL's version is one clause; MongoDB's needs an
explicit join stage plus an array-size check — noticeably more moving parts
for the same answer.

## Query 3: Aggregate — total spent per customer

```sql
-- SQL (Lesson 2.11)
SELECT c.name, COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spent
FROM customers c
LEFT JOIN orders o        ON o.customer_id = c.customer_id
LEFT JOIN order_items oi  ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```
```js
// MongoDB (Lesson 3.11)
db.customers.aggregate([
  { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } },
  { $project: { name: 1,
      total_spent: { $sum: { $map: {
          input: { $reduce: { input: "$orders.items", initialValue: [], in: { $concatArrays: ["$$value", "$$this"] } } },
          as: "item", in: { $multiply: ["$$item.quantity", "$$item.unit_price"] }
      }}}
  }},
  { $sort: { total_spent: -1 } }
]);
```
Both return: **Alice 3396.00, Bob 989.10 (at this point in the narrative),
Carla 0**. This is the clearest gap in this whole lesson — SQL's version
reads in one pass; MongoDB's needs `$reduce`/`$concatArrays`/`$map` just to
flatten nested arrays across documents before it can even sum them. This is
the direct cost of [Lesson 3.9](../03-mongodb/09-embedding-vs-referencing.md)'s
embedding choice — cheap for reading one order, expensive for aggregating
across many.

## Query 4: Group — average price per category

```sql
-- SQL (Lesson 2.8)
SELECT category, AVG(price) AS avg_price FROM products GROUP BY category;
```
```js
// MongoDB (Lesson 3.8)
db.products.aggregate([
  { $group: { _id: "$category", avg_price: { $avg: "$price" } } }
]);
```
Both return the same 5 category averages. Here they're nearly identical in
complexity — grouping and aggregating a *single* collection/table is one of
the closest matches between the two.

## What this shows, honestly

| Query shape | Complexity gap |
|---|---|
| Simple filter (Query 1) | None — nearly identical |
| Grouping one collection (Query 4) | None — nearly identical |
| Finding unmatched relationships (Query 2) | MongoDB needs more explicit steps |
| Aggregating across an embedded relationship (Query 3) | MongoDB needs noticeably more machinery |

The pattern: **the more a question spans multiple related records, the
bigger SQL's advantage gets** — because that's exactly what `JOIN` and
`GROUP BY` were built for. MongoDB's advantage shows up elsewhere, covered
next in [Lesson 4.3](03-pros-and-cons.md).

---
← [4.1 The Same Data, Two Ways](01-same-data-two-ways.md) | Next: [4.3 Pros and Cons →](03-pros-and-cons.md)
