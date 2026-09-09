← [3.6 Sort, Limit, Skip](06-sort-limit-skip.md)

# 3.7 Aggregation Functions

Same idea as [Lesson 2.7](../02-sql/07-functions.md) — computing something
from stored data, not just retrieving it as-is. In MongoDB, these live
inside an **aggregation pipeline** — a list of processing stages a
collection's documents flow through.

## Step 1 — Aggregate functions, summarizing the whole collection

```js
db.products.aggregate([
  { $group: {
      _id: null,
      count: { $sum: 1 },
      totalStock: { $sum: "$stock" },
      avgPrice: { $avg: "$price" }
  }}
]);
```
```
{ _id: null, count: 8, totalStock: 3050, avgPrice: 972.775 }
```

`_id: null` means "one group containing everything" — the MongoDB way of
saying "no `GROUP BY`, just summarize the whole collection," matching
[Lesson 2.7](../02-sql/07-functions.md)'s `SELECT COUNT(*), SUM(stock),
AVG(price) FROM products;` exactly, down to the same numbers.

| Accumulator | Does |
|---|---|
| `$sum: 1` | Counts documents |
| `$sum: "$field"` | Totals a numeric field |
| `$avg: "$field"` | Averages a numeric field |
| `$min` / `$max` | Smallest / largest value |

## Step 2 — Rounding: `$round`

```js
db.products.aggregate([
  { $group: { _id: null, avgPrice: { $avg: "$price" } } },
  { $project: { avgPrice: { $round: ["$avgPrice", 2] } } }
]);
```
```
{ avgPrice: 972.78 }
```

Same fix as [Lesson 2.7](../02-sql/07-functions.md)'s `ROUND(AVG(price), 2)`
— MongoDB just needs a second pipeline stage (`$project`) to reshape the
result, since `$round` isn't itself an accumulator.

Other math operators work the same way: `$ceil`, `$floor`, `$abs`.

## Step 3 — String operators

```js
db.products.aggregate([
  { $match: { _id: 1 } },
  { $project: { upper: { $toUpper: "$name" } } }
]);
```
```
{ upper: "IPHONE 17 PRO" }
```

| Operator | Does |
|---|---|
| `$toUpper` / `$toLower` | Case conversion |
| `$strLenCP` | String length |
| `$concat: ["$name", " (", "$category", ")"]` | Glue text together |
| `$substrCP` | Extract a substring |

`$match` here is the pipeline's equivalent of `WHERE` — filters *which*
documents enter the pipeline, always placed as early as possible.

## Step 4 — Date operators

```js
db.products.aggregate([
  { $match: { _id: 1 } },
  { $project: { year: { $year: "$created_at" } } }
]);
```
```
{ year: 2026 }
```

`$year`, `$month`, `$dayOfMonth`, and friends extract one part of a date —
the direct equivalent of SQL's `EXTRACT(YEAR FROM created_at)` from
[Lesson 2.7](../02-sql/07-functions.md).

## Step 5 — `$ifNull`: a default value for missing data

```js
db.customers.aggregate([
  { $project: { name: 1, phone: { $ifNull: ["$phone", "no phone provided"] } } }
]);
```

Direct equivalent of SQL's `COALESCE(phone, 'no phone provided')` — returns
the first non-null/non-missing value.

## Recap

| SQL ([Lesson 2.7](../02-sql/07-functions.md)) | MongoDB |
|---|---|
| `COUNT(*)`, `SUM`, `AVG`, `MIN`, `MAX` | `$sum`, `$avg`, `$min`, `$max` inside `$group` |
| `ROUND` | `$round` |
| `UPPER`/`LOWER`/`\|\|`/`LENGTH` | `$toUpper`/`$toLower`/`$concat`/`$strLenCP` |
| `EXTRACT(YEAR FROM ...)` | `$year` |
| `COALESCE` | `$ifNull` |

---
← [3.6 Sort, Limit, Skip](06-sort-limit-skip.md) | Next: [3.8 The `$group` Stage →](08-group-stage.md)
