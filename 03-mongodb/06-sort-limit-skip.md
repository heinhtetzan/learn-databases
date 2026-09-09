← [3.5 Query Operators](05-query-operators.md)

# 3.6 Sort, Limit, Skip

Same job as [Lesson 2.6](../02-sql/06-sort.md) — controlling order, and
grabbing just a slice of the results — same product data throughout.

## Step 1 — `.sort()`

```js
db.products.find().sort({ price: 1 });    // 1 = ascending
```
| name | price |
|---|---|
| AirPods Max | 549.00 |
| iPad Air | 599.00 |
| Mac Mini | 599.00 |
| MacBook Air | 989.10 |
| iPad Pro | 999.00 |
| iPhone 17 | 999.00 |
| iPhone 17 Pro | 1249.00 |
| MacBook Pro | 1799.10 |

```js
db.products.find().sort({ price: -1 });   // -1 = descending
```

## Step 2 — Ties: sort by more than one field

Same tie problem as [Lesson 2.6](../02-sql/06-sort.md) — `iPad Air`/`Mac Mini`
(both 599.00) and `iPad Pro`/`iPhone 17` (both 999.00). Fix it the same way,
with a second sort field:

```js
db.products.find().sort({ category: 1, price: -1 });
```
| name | category | price |
|---|---|---|
| AirPods Max | audio | 549.00 |
| Mac Mini | desktop | 599.00 |
| MacBook Pro | laptop | 1799.10 |
| MacBook Air | laptop | 989.10 |
| iPhone 17 Pro | smartphone | 1249.00 |
| iPhone 17 | smartphone | 999.00 |
| iPad Pro | tablet | 999.00 |
| iPad Air | tablet | 599.00 |

## Step 3 — `.limit()` and `.skip()`

```js
db.products.find().sort({ price: -1 }).limit(3);
```
| name | price |
|---|---|
| MacBook Pro | 1799.10 |
| iPhone 17 Pro | 1249.00 |
| iPad Pro | 999.00 |

Same tie as [Lesson 2.6](../02-sql/06-sort.md) noted for that last row — add
`_id` as a tiebreaker for a fully deterministic "top 3":

```js
db.products.find().sort({ price: -1, _id: 1 }).limit(3);
```

```js
db.products.find().sort({ price: -1 }).limit(3).skip(3);
```
Skips the first 3, returns the next 3 — "page 2," same pattern as SQL's
`LIMIT 3 OFFSET 3`.

## Step 4 — Combining a filter with sort and limit

```js
db.products.find({ category: { $ne: "smartphone" } })
  .sort({ price: 1 })
  .limit(3);
```
| name | category | price |
|---|---|---|
| AirPods Max | audio | 549.00 |
| iPad Air | tablet | 599.00 |
| Mac Mini | desktop | 599.00 |

Identical result to [Lesson 2.6](../02-sql/06-sort.md)'s SQL version — filter,
then sort, then take a slice, chained as method calls instead of clauses.

## Recap

| SQL ([Lesson 2.6](../02-sql/06-sort.md)) | MongoDB |
|---|---|
| `ORDER BY price ASC` | `.sort({ price: 1 })` |
| `ORDER BY price DESC` | `.sort({ price: -1 })` |
| `ORDER BY category, price DESC` | `.sort({ category: 1, price: -1 })` |
| `LIMIT 3` | `.limit(3)` |
| `LIMIT 3 OFFSET 3` | `.limit(3).skip(3)` |

---
← [3.5 Query Operators](05-query-operators.md) | Next: [3.7 Aggregation Functions →](07-aggregation-functions.md)
