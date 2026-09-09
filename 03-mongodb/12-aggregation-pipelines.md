← [3.11 `$lookup` (Joining Collections)](11-lookup-joins.md)

# 3.12 Aggregation Pipelines

[Lesson 2.12](../02-sql/12-subqueries-and-ctes.md) built queries from
smaller pieces — "first find X, then use it to find Y." Every aggregation
you've written since [Lesson 3.7](07-aggregation-functions.md) has already
been doing exactly that: **a pipeline is a chain of stages, each one working
on the previous stage's output.**

## Step 1 — You've been writing "CTEs" all along

```js
db.products.aggregate([
  { $group: { _id: "$category", avgPrice: { $avg: "$price" } } },   // "Step 1: compute this"
  { $match: { avgPrice: { $gt: 700 } } }                             // "Step 2: filter it"
]);
```

This *is* [Lesson 2.12](../02-sql/12-subqueries-and-ctes.md)'s
`category_stats` CTE — no special keyword needed; every pipeline is already
built from named, ordered steps, each one reading only what the step before
it produced.

## Step 2 — `$facet`: several "subqueries" side by side, in one round trip

```js
db.products.aggregate([
  { $facet: {
      cheapest: [{ $sort: { price: 1 } }, { $limit: 1 }],
      mostExpensive: [{ $sort: { price: -1 } }, { $limit: 1 }],
      byCategory: [{ $group: { _id: "$category", count: { $sum: 1 } } }]
  }}
]);
```

`$facet` runs multiple independent mini-pipelines against the *same* input
documents, all in one call — something SQL can only do with several separate
subqueries or CTEs referencing the same base table. There's no single SQL
line-for-line equivalent; it's a genuinely MongoDB-shaped tool.

## Step 3 — `$graphLookup`: the recursive CTE equivalent

[Lesson 2.12](../02-sql/12-subqueries-and-ctes.md)'s bonus section built a
staff org chart with `WITH RECURSIVE`. Same data, same question, in MongoDB:

```js
db.employees.insertMany([
  { _id: 1, name: "Sarah Kim",   manager_id: null },
  { _id: 2, name: "Tom Reyes",   manager_id: 1 },
  { _id: 3, name: "Priya Patel", manager_id: 2 },
  { _id: 4, name: "Jake Chen",   manager_id: 3 },
  { _id: 5, name: "Mia Torres",  manager_id: 3 }
]);

db.employees.aggregate([
  { $match: { _id: 1 } },
  { $graphLookup: {
      from: "employees",
      startWith: "$_id",
      connectFromField: "_id",
      connectToField: "manager_id",
      as: "reports",
      depthField: "depth"
  }}
]);
```
```
{
  _id: 1, name: "Sarah Kim", manager_id: null,
  reports: [
    { _id: 2, name: "Tom Reyes",   depth: 0 },
    { _id: 3, name: "Priya Patel", depth: 1 },
    { _id: 4, name: "Jake Chen",   depth: 2 },
    { _id: 5, name: "Mia Torres",  depth: 2 }
  ]
}
```

Same 4 people found, at the same relative depths as
[Lesson 2.12](../02-sql/12-subqueries-and-ctes.md)'s SQL result — one
notable difference: `$graphLookup` returns Sarah's own document with
`reports` **attached to it**, rather than one flat table including Sarah
herself at `depth: 1`. No `UNION ALL`, no explicit anchor/recursive-step
split — `$graphLookup` handles the "however many levels deep" traversal in
a single stage.

## Step 4 — Recap

| SQL ([Lesson 2.12](../02-sql/12-subqueries-and-ctes.md)) | MongoDB |
|---|---|
| Subquery / CTE | A pipeline stage, feeding the next stage |
| Multiple independent subqueries on the same table | `$facet` |
| `WITH RECURSIVE` (org charts, hierarchies) | `$graphLookup` |
| `EXISTS` / `NOT EXISTS` | `$lookup` + `$match` on array size (Lesson 3.11) |

---
← [3.11 `$lookup` (Joining Collections)](11-lookup-joins.md) | Next: [3.13 Schema Validation →](13-schema-validation.md)
