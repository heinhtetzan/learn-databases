← [3.2 Your First Database](02-your-first-database-apple-example.md)

# 3.3 Types of MongoDB Operations

Before any syntax, 3 real-world situations that need very different *kinds*
of MongoDB operations — echoing [Lesson 2.3](../02-sql/03-types-of-sql-queries.md)'s
SQL categories.

## 3 real-world scenarios

**1. An online store** inserts new products constantly, and reads them far
more often than it writes them — two very different jobs against the same
collection.

**2. A hospital IT admin** grants a new nurse's MongoDB account read-only
access to patient records, without letting them drop a collection.

**3. A bank's MongoDB-backed ledger** must reserve funds and record a
transaction together, or not at all — the same all-or-nothing need from
[Lesson 2.14](../02-sql/14-transactions.md), now in a document database.

## The 5 categories, mapped from SQL

| SQL category ([Lesson 2.3](../02-sql/03-types-of-sql-queries.md)) | MongoDB equivalent |
|---|---|
| DDL (`CREATE`, `ALTER`, `DROP`) | Collection & index management |
| DML (`INSERT`, `UPDATE`, `DELETE`) | `insertOne`/`updateOne`/`deleteOne` and their bulk versions |
| DQL (`SELECT`) | `find()` and the aggregation pipeline |
| DCL (`GRANT`, `REVOKE`) | `db.createUser()`, roles |
| TCL (`BEGIN`, `COMMIT`, `ROLLBACK`) | Sessions and multi-document transactions |

## Step 1 — Collection & index management

```js
db.createCollection("orders");        // rarely needed — usually created implicitly
db.orders.createIndex({ customer_id: 1 });
db.orders.drop();                     // deletes the whole collection
```

## Step 2 — CRUD (Create, Read, Update, Delete)

Already used throughout [Lesson 3.2](02-your-first-database-apple-example.md):

```js
db.products.insertOne({ ... });
db.products.find({ category: "laptop" });
db.products.updateOne({ _id: 1 }, { $set: { price: 1249.00 } });
db.products.deleteOne({ _id: 6 });
```

## Step 3 — Queries and aggregation (reading)

```js
db.products.find({ price: { $gt: 1000 } });   // simple query
db.products.aggregate([
  { $group: { _id: "$category", avgPrice: { $avg: "$price" } } }
]);                                             // multi-stage pipeline — Lesson 3.12
```

## Step 4 — User & role management

```js
db.createUser({
  user: "app_user",
  pwd: "change_me_123",
  roles: [{ role: "readWrite", db: "apple_store" }]
});
```

Covered fully in [Lesson 3.18](18-user-access-management.md) — the direct
counterpart of [Lesson 2.18](../02-sql/18-user-access-management.md)'s
`GRANT`/`REVOKE`.

## Step 5 — Transactions

```js
const session = db.getMongo().startSession();
session.startTransaction();
try {
  db.orders.insertOne({ ... }, { session });
  db.products.updateOne({ _id: 1 }, { $inc: { stock: -1 } }, { session });
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

Covered fully in [Lesson 3.14](14-transactions.md).

## Recap

| Category | MongoDB tools |
|---|---|
| Structure | `createCollection`, `createIndex`, `drop` |
| Write | `insertOne`/`Many`, `updateOne`/`Many`, `deleteOne`/`Many` |
| Read | `find()`, `aggregate()` |
| Access control | `createUser`, roles |
| Safety/grouping | Sessions + `startTransaction`/`commitTransaction`/`abortTransaction` |

Same 5 jobs as SQL — different names, same underlying needs.

---
← [3.2 Your First Database](02-your-first-database-apple-example.md) | Next: [3.4 Data Types in MongoDB →](04-data-types.md)
