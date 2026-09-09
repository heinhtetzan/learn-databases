← [3.14 Transactions](14-transactions.md)

# 3.15 Indexes & Performance

Same 3 scenarios as [Lesson 2.15](../02-sql/15-indexes-and-performance.md) —
a search engine, a shop's product search, a hospital's emergency lookup, all
needing to avoid scanning millions of documents one by one.

## Step 1 — Same underlying structure: a B-Tree

MongoDB's default index type is a **B-Tree** — the exact same structure from
[Lesson 2.15](../02-sql/15-indexes-and-performance.md):

![B-Tree Index](../assets/images/btree-index.png)

Everything that diagram taught still applies: root → internal nodes →
sorted leaf pages, letting MongoDB jump straight to matching documents
instead of scanning every one.

## Step 2 — What's already indexed, and what isn't

`_id` is **automatically** indexed on every collection — same as SQL's
`PRIMARY KEY`. Nothing else is, including reference fields:

```js
db.orders.createIndex({ customer_id: 1 });
db.orders.createIndex({ "items.product_id": 1 });   // can index INSIDE embedded arrays too
```

That second line is worth noticing — you can index a field nested inside an
embedded array, something SQL's flat columns have no equivalent for.

## Step 3 — Reading `.explain()`

```js
db.orders.find({ customer_id: 1 }).explain("executionStats");
```
```
winningPlan: { stage: "COLLSCAN" }    // scanned every document
```

Just like [Lesson 2.15](../02-sql/15-indexes-and-performance.md)'s honest
example on a tiny table — `COLLSCAN` (collection scan, MongoDB's version of
`Seq Scan`) is often genuinely correct on a small collection like ours, even
with an index sitting right there unused. On a large collection, the same
query would instead show:

```
-- Illustrative: same query, on a collection with millions of documents
winningPlan: { stage: "IXSCAN", indexName: "customer_id_1" }
```

`IXSCAN` is MongoDB's `Index Scan` — jumping straight to matching documents.

## Step 4 — Compound indexes and field order

```js
db.products.createIndex({ category: 1, price: 1 });
```

Identical rule to [Lesson 2.15](../02-sql/15-indexes-and-performance.md)'s
composite index: this efficiently supports `find({ category: "laptop" })`
and `find({ category: "laptop", price: { $gt: 1000 } })`, but not
`find({ price: { $gt: 1000 } })` alone — put the equality field first, range
fields after.

## Step 5 — When an index doesn't help

Same list as [Lesson 2.15](../02-sql/15-indexes-and-performance.md): small
collections, low-cardinality fields, queries returning most of the
collection anyway, and collections written to far more than read — every
index also slows down every `insertOne`/`updateOne`/`deleteOne`, since
MongoDB has to keep it up to date too.

## Recap

| SQL ([Lesson 2.15](../02-sql/15-indexes-and-performance.md)) | MongoDB |
|---|---|
| B-Tree index | Same structure, same default index type |
| `PRIMARY KEY` auto-indexed | `_id` auto-indexed |
| `CREATE INDEX` | `createIndex()` |
| `EXPLAIN` | `.explain("executionStats")` |
| `Seq Scan` | `COLLSCAN` |
| `Index Scan` | `IXSCAN` |
| Composite index, column order matters | Compound index, field order matters, same rule |

---
← [3.14 Transactions](14-transactions.md) | Next: [3.16 Views →](16-views.md)
