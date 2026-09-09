← [3.15 Indexes & Performance](15-indexes-and-performance.md)

# 3.16 Views

Same idea as [Lesson 2.16](../02-sql/16-views.md) — a saved query you can
read from like a real collection, without re-typing it every time.

## Step 1 — Where our data stands after Lesson 3.14

Same final totals as [Lesson 2.16](../02-sql/16-views.md)'s SQL version:
Alice **3396.00**, Bob **2788.20**, Carla **1198.00**.

## Step 2 — Creating a view

```js
db.createView(
  "customer_order_summary",
  "customers",
  [
    { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } },
    { $project: {
        name: 1,
        total_spent: {
          $sum: { $map: {
            input: { $reduce: { input: "$orders.items", initialValue: [], in: { $concatArrays: ["$$value", "$$this"] } } },
            as: "item",
            in: { $multiply: ["$$item.quantity", "$$item.unit_price"] }
          }}
        }
    }}
  ]
);
```

`db.createView(name, source_collection, pipeline)` takes exactly the
aggregation pipeline from [Lesson 3.11](11-lookup-joins.md)'s bonus step and
saves it under a name — a MongoDB view *is* a saved aggregation pipeline,
nothing more.

## Step 3 — Querying a view like a normal collection

```js
db.customer_order_summary.find().sort({ total_spent: -1 });
```
| name | total_spent |
|---|---|
| Alice Chen | 3396.00 |
| Bob Diaz | 2788.20 |
| Carla Ruiz | 0 |

```js
db.customer_order_summary.find({ total_spent: { $gt: 2000 } });
```
| name | total_spent |
|---|---|
| Alice Chen | 3396.00 |
| Bob Diaz | 2788.20 |

You can `find()`, filter, and sort against a view exactly like a real
collection — the multi-stage pipeline behind it stays hidden.

## Step 4 — Why bother

Same reasons as [Lesson 2.16](../02-sql/16-views.md): consistency (one
definition, used everywhere), simplicity (a teammate queries
`customer_order_summary`, not the raw `$lookup`/`$reduce` pipeline), and
access control (a role can be granted read access to the view without
touching the underlying collections — see [Lesson 3.18](18-user-access-management.md)).

## Step 5 — Views are always read-only

```js
db.customer_order_summary.updateOne({ name: "Carla Ruiz" }, { $set: { total_spent: 5000 } });
// CommandNotSupportedOnView
```

Unlike SQL's nuance (a *simple*, single-table view can sometimes be
updatable — [Lesson 2.16](../02-sql/16-views.md), Step 5), a MongoDB view is
**always** read-only, no exceptions. Update the real `customers`/`orders`
collections directly instead.

## Step 6 — No materialized view — but `$merge`/`$out` come close

MongoDB has no `CREATE MATERIALIZED VIEW`. The closest equivalent: run an
aggregation and write its result into a **real collection** with `$merge`:

```js
db.customers.aggregate([
  { $lookup: { from: "orders", localField: "_id", foreignField: "customer_id", as: "orders" } },
  { $project: { name: 1, total_spent: 1 } },
  { $merge: { into: "customer_order_summary_cached" } }
]);
```

Same tradeoff as [Lesson 2.16](../02-sql/16-views.md)'s materialized view —
faster to read, goes stale until you re-run the aggregation.

## Recap

| SQL ([Lesson 2.16](../02-sql/16-views.md)) | MongoDB |
|---|---|
| `CREATE VIEW` | `db.createView(name, source, pipeline)` |
| Regular view | A saved aggregation pipeline |
| Materialized view | `$merge`/`$out` into a real collection |
| Sometimes updatable | **Never** updatable |

---
← [3.15 Indexes & Performance](15-indexes-and-performance.md) | Next: [3.17 Create Collections: More Examples →](17-create-collections-examples.md)
