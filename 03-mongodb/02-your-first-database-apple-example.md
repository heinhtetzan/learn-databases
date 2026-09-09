← [3.1 What Is MongoDB?](01-what-is-mongodb.md)

# 3.2 Your First Database: Storing Apple's Products

Same story as [Lesson 2.2](../02-sql/02-your-first-database-apple-example.md)
— you're storing Apple's product catalog — rebuilt from scratch in MongoDB,
ending at the **exact same data** so Chapter 4 can compare them directly.

## Step 1 — "Create" a database

```js
use apple_store
```

Unlike `CREATE DATABASE` in [Lesson 2.2](../02-sql/02-your-first-database-apple-example.md),
this doesn't actually create anything yet — MongoDB creates the database (and
any collection) automatically, the moment you first insert into it.

## Step 2 — No `CREATE TABLE` step

There's no equivalent of [Lesson 2.2](../02-sql/02-your-first-database-apple-example.md)'s
Step 2 at all. A **collection** (MongoDB's rough equivalent of a table) isn't
declared up front with fixed columns — it springs into existence on your
first `insertOne`/`insertMany`, and every document in it can have a
different shape. (Whether that's a good idea is exactly what
[Lesson 3.9](09-embedding-vs-referencing.md) digs into.)

## Step 3 — Insert data

### 3a. Insert a single document first

```js
db.products.insertOne({
  _id: 1,
  name: "iPhone 17 Pro",
  category: "smartphone",
  price: 1249.00,
  stock: 500,
  created_at: new Date(),
  updated_at: new Date()
});
```

Using a plain integer for `_id` (instead of letting MongoDB generate its
default `ObjectId`) is a deliberate choice here — it keeps `_id` matching
[Lesson 2.2](../02-sql/02-your-first-database-apple-example.md)'s
`product_id` exactly, which makes every comparison in Chapter 4 much easier
to follow.

### 3b. Insert multiple documents at once

```js
db.products.insertMany([
  { _id: 2,  name: "MacBook Air",           category: "laptop",      price: 1099.00, stock: 300,  created_at: new Date(), updated_at: new Date() },
  { _id: 3,  name: "MacBook Pro",           category: "laptop",      price: 1999.00, stock: 200,  created_at: new Date(), updated_at: new Date() },
  { _id: 4,  name: "iPad Air",              category: "tablet",      price: 599.00,  stock: 400,  created_at: new Date(), updated_at: new Date() },
  { _id: 5,  name: "iPad Pro",              category: "tablet",      price: 999.00,  stock: 350,  created_at: new Date(), updated_at: new Date() },
  { _id: 6,  name: "AirPods Pro",           category: "audio",       price: 249.00,  stock: 1000, created_at: new Date(), updated_at: new Date() },
  { _id: 7,  name: "AirPods Max",           category: "audio",       price: 549.00,  stock: 250,  created_at: new Date(), updated_at: new Date() },
  { _id: 8,  name: "Apple Watch Series 11", category: "wearable",    price: 399.00,  stock: 700,  created_at: new Date(), updated_at: new Date() },
  { _id: 9,  name: "Apple TV 4K",           category: "accessory",   price: 129.00,  stock: 800,  created_at: new Date(), updated_at: new Date() },
  { _id: 10, name: "Mac Mini",              category: "desktop",     price: 599.00,  stock: 450,  created_at: new Date(), updated_at: new Date() },
  { _id: 11, name: "iPhone 17",             category: "smartphone",  price: 999.00,  stock: 600,  created_at: new Date(), updated_at: new Date() }
]);
```

One call, ten new documents — same idea as
[Lesson 2.2](../02-sql/02-your-first-database-apple-example.md)'s bulk
`INSERT`. The collection now holds 11 documents total.

## Step 4 — Retrieve data

```js
db.products.find();                                   // every document
db.products.find({ category: "laptop" });              // just the laptops
db.products.find({ price: { $lt: 300 } });              // anything under $300
db.products.find().sort({ price: 1 });                  // cheapest to most expensive
```

`find({ category: "laptop" })` is the direct equivalent of
[Lesson 2.5](../02-sql/05-operators.md)'s `WHERE category = 'laptop'` — one
plain object instead of a `WHERE` clause. `$lt` (less than) is the first of
several **query operators**, covered fully in [Lesson 3.5](05-query-operators.md).

## Step 5 — Delete data

### 5a. Delete a single document

```js
// Option A: filter by _id (recommended)
db.products.deleteOne({ _id: 6 });

// Option B: filter by name
db.products.deleteOne({ name: "AirPods Pro" });
```

Same reasoning as [Lesson 2.5](../02-sql/05-operators.md)'s SQL version:
`_id` is guaranteed unique and stable; `name` is fine for a quick lookup.

### 5b. Delete multiple documents at once

```js
db.products.deleteMany({ _id: { $in: [8, 9] } });
```

`$in` is MongoDB's version of SQL's `IN (...)` from
[Lesson 2.5](../02-sql/05-operators.md) — removes Apple Watch Series 11 and
Apple TV 4K together, in one call.

## Step 6 — Update data

### 6a. Update a single document

```js
db.products.updateOne(
  { _id: 1 },
  { $set: { price: 1249.00 }, $currentDate: { updated_at: true } }
);
```

Every update needs `$set` (or another update operator) — unlike SQL's
`UPDATE ... SET`, you can't just assign a field directly; MongoDB always
expects to be told *how* you're changing the document. `$currentDate` is the
direct equivalent of `updated_at = CURRENT_TIMESTAMP` from
[Lesson 2.2](../02-sql/02-your-first-database-apple-example.md).

### 6b. Update multiple documents at once

```js
db.products.updateMany(
  { category: "laptop" },
  [{ $set: { price: { $multiply: ["$price", 0.9] } } }, { $set: { updated_at: "$$NOW" } }]
);
```

Same 10% discount as [Lesson 2.6](../02-sql/06-sort.md)'s SQL version, applied
to every `laptop` at once — `$multiply` reads each document's *own* current
price, same as SQL's `price = price * 0.9`.

## Step 7 — Where our data stands now

```js
db.products.find().sort({ _id: 1 });
```
| _id | name | category | price | stock |
|---|---|---|---|---|
| 1 | iPhone 17 Pro | smartphone | 1249.00 | 500 |
| 2 | MacBook Air | laptop | 989.10 | 300 |
| 3 | MacBook Pro | laptop | 1799.10 | 200 |
| 4 | iPad Air | tablet | 599.00 | 400 |
| 5 | iPad Pro | tablet | 999.00 | 350 |
| 7 | AirPods Max | audio | 549.00 | 250 |
| 10 | Mac Mini | desktop | 599.00 | 450 |
| 11 | iPhone 17 | smartphone | 999.00 | 600 |

**Identical data** to [Lesson 2.5](../02-sql/05-operators.md)'s SQL table —
that's deliberate, and every lesson from here uses it.

## Step 8 — Recap

| Step | SQL equivalent | MongoDB |
|---|---|---|
| Create database | `CREATE DATABASE` | `use apple_store` |
| Create table/collection | `CREATE TABLE` | Nothing — created on first insert |
| Insert one | `INSERT` (single) | `insertOne()` |
| Insert many | `INSERT` (bulk) | `insertMany()` |
| Retrieve | `SELECT` | `find()` |
| Delete one/many | `DELETE ... WHERE` | `deleteOne()` / `deleteMany()` |
| Update one/many | `UPDATE ... SET` | `updateOne()` / `updateMany()` |

---
← [3.1 What Is MongoDB?](01-what-is-mongodb.md) | Next: [3.3 Types of MongoDB Operations →](03-types-of-mongodb-operations.md)
