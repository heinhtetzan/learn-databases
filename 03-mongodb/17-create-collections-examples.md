← [3.16 Views](16-views.md)

# 3.17 Create Collections: More Examples

Same idea as [Lesson 2.17](../02-sql/17-create-tables-examples.md) — more
practice with fresh domains, plus a couple of capabilities SQL has no
equivalent for at all.

## Step 1 — A simple standalone collection: tasks

```js
db.createCollection("tasks", {
  validator: {
    $jsonSchema: {
      required: ["title", "priority"],
      properties: {
        is_done:  { bsonType: "bool" },
        due_date: { bsonType: "date" },
        priority: { enum: ["low", "medium", "high"] }
      }
    }
  }
});

db.tasks.insertMany([
  { title: "Restock AirPods Max", due_date: ISODate("2026-04-01"), priority: "high", is_done: false },
  { title: "Update store hours page", priority: "low", is_done: false }
]);
```

Same `enum` pattern as [Lesson 3.13](13-schema-validation.md) standing in
for SQL's `CHECK (priority IN (...))`.

## Step 2 — A fresh domain: a small blog

```js
db.authors.insertOne({ _id: 1, name: "Priya Patel" });

db.posts.insertMany([
  { _id: 1, author_id: 1, title: "Hello World", slug: "hello-world",
    body: "Our first post!", published_at: ISODate("2026-03-01T09:00:00Z") },
  { _id: 2, author_id: 1, title: "Upcoming Sale", slug: "upcoming-sale",
    body: "Draft — details TBD", published_at: null }   // null = still a draft
]);

db.posts.createIndex({ slug: 1 }, { unique: true });
```

Same design choice as [Lesson 2.17](../02-sql/17-create-tables-examples.md):
`published_at: null` means "draft," rather than a separate boolean field
that could disagree with the actual date.

## Step 3 — Referencing back to `products`

```js
db.warehouses.insertMany([
  { _id: 1, city: "Austin" },
  { _id: 2, city: "Newark" }
]);

db.inventory.insertMany([
  { warehouse_id: 1, product_id: 1, quantity: 120 },
  { warehouse_id: 2, product_id: 1, quantity: 80 }
]);

db.inventory.createIndex({ warehouse_id: 1, product_id: 1 }, { unique: true });
```

A compound unique index is the MongoDB equivalent of
[Lesson 2.17](../02-sql/17-create-tables-examples.md)'s composite
`PRIMARY KEY (warehouse_id, product_id)` — same guarantee, same reasoning.

## Step 4 — Snapshotting data: `$out`

```js
db.products.aggregate([
  { $match: {} },
  { $out: "products_snapshot_2026_q1" }
]);
```

Direct equivalent of SQL's `CREATE TABLE ... AS SELECT` — freezes the
current data into a brand-new, independent collection that later changes to
`products` will never touch.

## Step 5 — Two capabilities SQL has no equivalent for

**Capped collections** — a fixed-size collection that automatically deletes
its *oldest* documents once full, keeping insertion order without you ever
running a manual cleanup:

```js
db.createCollection("recent_activity", { capped: true, size: 1048576, max: 1000 });
```

Ideal for logs or activity feeds where you only ever care about "the last
N events," and don't want them accumulating forever.

**TTL (time-to-live) indexes** — documents that delete themselves
automatically after a set time:

```js
db.sessions.createIndex({ created_at: 1 }, { expireAfterSeconds: 3600 });
```

Any `sessions` document older than 1 hour is removed automatically by
MongoDB in the background — no cron job, no manual `DELETE ... WHERE
created_at < ...` needed.

## Recap

| Technique | Where |
|---|---|
| Schema validation on a new collection | Step 1 |
| Nullable field as a meaningful state | Step 2 |
| Compound unique index (composite key equivalent) | Step 3 |
| `$out` (snapshot, not live) | Step 4 |
| Capped collection (SQL has no equivalent) | Step 5 |
| TTL index (SQL has no equivalent) | Step 5 |

---
← [3.16 Views](16-views.md) | Next: [3.18 User & Access Management →](18-user-access-management.md)
