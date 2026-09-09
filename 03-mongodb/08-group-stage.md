← [3.7 Aggregation Functions](07-aggregation-functions.md)

# 3.8 The `$group` Stage

Same job as [Lesson 2.8](../02-sql/08-group.md)'s `GROUP BY` — one summary
per category, not one for the whole collection.

## 3 real-world scenarios

Same 3 as [Lesson 2.8](../02-sql/08-group.md): total sales per category,
average GPA per department, patient count per doctor — every one needs a
result **bucketed**, not a single overall number.

## Step 1 — `$group` in practice

```js
db.products.aggregate([
  { $group: { _id: "$category", numProducts: { $sum: 1 } } }
]);
```
| _id (category) | numProducts |
|---|---|
| smartphone | 2 |
| laptop | 2 |
| tablet | 2 |
| audio | 1 |
| desktop | 1 |

`_id: "$category"` is what makes this a *grouped* aggregation instead of
[Lesson 3.7](07-aggregation-functions.md)'s single-group summary — every
document sharing the same `category` value collapses into one output
document, matching [Lesson 2.8](../02-sql/08-group.md)'s SQL result exactly.

## Step 2 — Multiple accumulators per group

```js
db.products.aggregate([
  { $group: { _id: "$category", totalValue: { $sum: "$price" }, avgPrice: { $avg: "$price" } } }
]);
```
| _id | totalValue | avgPrice |
|---|---|---|
| smartphone | 2248.00 | 1124.00 |
| laptop | 2788.20 | 1394.10 |
| tablet | 1598.00 | 799.00 |
| audio | 549.00 | 549.00 |
| desktop | 599.00 | 599.00 |

Identical numbers to [Lesson 2.8](../02-sql/08-group.md)'s SQL version.

## Step 3 — No "ungrouped column" trap

Unlike SQL's rule ([Lesson 2.8](../02-sql/08-group.md), Step 3 — every
`SELECT`ed column must be grouped or aggregated), MongoDB doesn't enforce
this at all: a `$group` stage's output documents *only* ever contain `_id`
plus whatever accumulators you defined — there's no way to accidentally
"forget" a column, because nothing outside the group definition survives
into the output.

## Step 4 — Filtering groups: the `HAVING` equivalent

MongoDB has no separate `HAVING` keyword — you just add another `$match`
stage **after** `$group`:

```js
db.products.aggregate([
  { $group: { _id: "$category", numProducts: { $sum: 1 } } },
  { $match: { numProducts: { $gt: 1 } } }
]);
```
| _id | numProducts |
|---|---|
| smartphone | 2 |
| laptop | 2 |
| tablet | 2 |

Same result as [Lesson 2.8](../02-sql/08-group.md)'s `HAVING COUNT(*) > 1` —
`audio` and `desktop` (1 product each) are filtered out.

## Step 5 — `$match` before *and* after `$group`

```js
db.products.aggregate([
  { $match: { stock: { $gt: 300 } } },
  { $group: { _id: "$category", avgPrice: { $avg: "$price" } } },
  { $match: { avgPrice: { $gt: 700 } } }
]);
```
| _id | avgPrice |
|---|---|
| smartphone | 1124.00 |
| tablet | 799.00 |

Same 3-step logic as [Lesson 2.8](../02-sql/08-group.md)'s combined
`WHERE`/`GROUP BY`/`HAVING` example, and the same final result: `laptop` and
`audio` lose all their rows in the first `$match` (stock 300, 200, 250 —
none exceed 300), so those groups never form at all; `desktop` forms but
gets filtered by the second `$match`.

## Recap

| SQL ([Lesson 2.8](../02-sql/08-group.md)) | MongoDB |
|---|---|
| `GROUP BY category` | `{ $group: { _id: "$category", ... } }` |
| `WHERE` (before grouping) | `$match` stage before `$group` |
| `HAVING` (after grouping) | `$match` stage after `$group` |
| Every `SELECT`ed column must be grouped/aggregated | Not applicable — `$group`'s output is only ever `_id` + accumulators |

---
← [3.7 Aggregation Functions](07-aggregation-functions.md) | Next: [3.9 Embedding vs. Referencing →](09-embedding-vs-referencing.md)
