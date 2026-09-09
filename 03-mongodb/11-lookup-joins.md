← [3.10 Relationships in MongoDB](10-relationships-in-mongodb.md)

# 3.11 `$lookup` (Joining Collections)

Same 3 scenarios as [Lesson 2.11](../02-sql/11-joins.md) — a shop needing
customer + order data together, a university needing students + courses,
a hospital needing patients + doctors + appointments. `$lookup` is
MongoDB's join.

## Step 1 — `$lookup`: the basic join

```js
db.orders.aggregate([
  { $lookup: { from: "customers", localField: "customer_id", foreignField: "_id", as: "customer" } },
  { $unwind: "$customer" },
  { $project: { _id: 1, "customer.name": 1, order_date: 1 } }
]);
```
| _id | customer.name | order_date |
|---|---|---|
| 1 | Alice Chen | 2026-03-01 |
| 2 | Bob Diaz | 2026-03-02 |
| 3 | Alice Chen | 2026-03-05 |

`$lookup` always adds the matched documents as an **array** field (`customer`
here) — `$unwind` then flattens that single-element array back into a plain
field, which is why almost every `$lookup` is immediately followed by
`$unwind` when you expect exactly one match.

## Step 2 — `$lookup` behaves like `LEFT JOIN` by default

```js
db.customers.aggregate([
  { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } }
]);
```
| name | orders |
|---|---|
| Alice Chen | `[order 1, order 3]` |
| Bob Diaz | `[order 2]` |
| Carla Ruiz | `[]` (empty array) |

Unlike SQL's `LEFT JOIN` ([Lesson 2.11](../02-sql/11-joins.md)), which fills
unmatched rows with `NULL` columns, `$lookup` keeps **every** customer and
gives Carla an **empty array**, not a missing/null field — worth remembering
since checking for "no match" looks different:

```js
db.customers.aggregate([
  { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } },
  { $match: { orders: { $size: 0 } } }
]);
```
| name |
|---|
| Carla Ruiz |

`{ orders: { $size: 0 } }` is the MongoDB equivalent of SQL's
`WHERE o.order_id IS NULL` trick.

## Step 3 — No dedicated `RIGHT JOIN` or `FULL OUTER JOIN`

Same fix as SQL's `RIGHT JOIN` note ([Lesson 2.11](../02-sql/11-joins.md)) —
just start the pipeline from the other collection. A true `FULL OUTER JOIN`
equivalent exists (`$unionWith` combined with two opposite `$lookup`s), but
it's rare enough in practice that most teams restructure the question
instead of reaching for it.

## Step 4 — Joining 3 collections, through an embedded array

```js
db.orders.aggregate([
  { $unwind: "$items" },
  { $lookup: { from: "customers", localField: "customer_id", foreignField: "_id", as: "customer" } },
  { $unwind: "$customer" },
  { $lookup: { from: "products", localField: "items.product_id", foreignField: "_id", as: "product" } },
  { $unwind: "$product" },
  { $project: {
      customer: "$customer.name",
      order_id: "$_id",
      product: "$product.name",
      quantity: "$items.quantity",
      unit_price: "$items.unit_price",
      line_total: { $multiply: ["$items.quantity", "$items.unit_price"] }
  }},
  { $sort: { order_id: 1 } }
]);
```
| customer | order_id | product | quantity | unit_price | line_total |
|---|---|---|---|---|---|
| Alice Chen | 1 | iPhone 17 Pro | 1 | 1249.00 | 1249.00 |
| Alice Chen | 1 | AirPods Max | 1 | 549.00 | 549.00 |
| Bob Diaz | 2 | MacBook Air | 1 | 989.10 | 989.10 |
| Alice Chen | 3 | iPad Pro | 1 | 999.00 | 999.00 |
| Alice Chen | 3 | Mac Mini | 1 | 599.00 | 599.00 |

Same result as [Lesson 2.11](../02-sql/11-joins.md)'s SQL join — but notice
the extra step: `$unwind: "$items"` had to come first, to turn each order's
*embedded array* of items into separate documents the pipeline could join
against individually.

## Step 5 — Bonus: total spent per customer (the honest, harder version)

```js
db.customers.aggregate([
  { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } },
  { $project: {
      name: 1,
      total_spent: {
        $sum: {
          $map: {
            input: { $reduce: {
              input: "$orders.items", initialValue: [],
              in: { $concatArrays: ["$$value", "$$this"] }
            }},
            as: "item",
            in: { $multiply: ["$$item.quantity", "$$item.unit_price"] }
          }
        }
      }
  }},
  { $sort: { total_spent: -1 } }
]);
```
| name | total_spent |
|---|---|
| Alice Chen | 3396.00 |
| Bob Diaz | 989.10 |
| Carla Ruiz | 0 |

Same numbers as [Lesson 2.11](../02-sql/11-joins.md)'s SQL version — but
worth being honest about the cost: SQL solved this with a `JOIN` + `SUM` +
`GROUP BY`. Here, each customer's `orders` embeds an *array of arrays* of
items (one items-array per order), so getting one flat total requires
`$reduce` to flatten them, then `$map` to compute each line's value, then
`$sum` to total it. **This is the real tradeoff from embedding**: reading a
single order is trivial (Step 4 was easy for a *known* order), but
aggregating *across* many documents' embedded arrays is genuinely more
complex than SQL's equivalent.

## Recap

| SQL ([Lesson 2.11](../02-sql/11-joins.md)) | MongoDB |
|---|---|
| `INNER JOIN` | `$lookup` + `$unwind` (drops unmatched, since `$unwind` skips empty arrays) |
| `LEFT JOIN` | `$lookup` alone (always keeps every source document) |
| `WHERE ... IS NULL` (find unmatched) | `$match: { field: { $size: 0 } }` |
| Multi-table join | Multiple `$lookup` stages, `$unwind`ing embedded arrays as needed |
| Join + `SUM`/`GROUP BY` | Often needs `$reduce`/`$map` to flatten embedded arrays first |

---
← [3.10 Relationships in MongoDB](10-relationships-in-mongodb.md) | Next: [3.12 Aggregation Pipelines →](12-aggregation-pipelines.md)
