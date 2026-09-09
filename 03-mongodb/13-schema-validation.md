← [3.12 Aggregation Pipelines](12-aggregation-pipelines.md)

# 3.13 Schema Validation

Same 3 scenarios as [Lesson 2.13](../02-sql/13-constraints.md) — a bank that
must never allow a negative balance, a hospital that must never allow
duplicate license numbers, a shop that must never reference a nonexistent
product. MongoDB has tools for some of these — not all.

## Step 1 — `_id`: always unique, always indexed

Every collection automatically enforces uniqueness on `_id` — the direct
equivalent of SQL's `PRIMARY KEY`, with zero setup required.

```js
db.products.insertOne({ _id: 1, name: "Duplicate!" });
// E11000 duplicate key error — _id: 1 already exists
```

## Step 2 — Foreign keys: already covered, still not enforced

[Lesson 3.10](10-relationships-in-mongodb.md) already showed this gap in
full — nothing here changes it. Schema validation (below) can check a
field's *type*, but never that its value exists in another collection.

## Step 3 — `UNIQUE`: a unique index

```js
db.customers.createIndex({ email: 1 }, { unique: true });

db.customers.insertOne({ _id: 4, name: "David Kim", email: "alice@mail.com", city: "Boston" });
// E11000 duplicate key error collection: apple_store.customers index: email_1
// dup key: { email: "alice@mail.com" }
```

Same mechanism as `_id`'s built-in uniqueness — just applied to a different
field, explicitly.

## Step 4 — `CHECK`-style rules: `$jsonSchema` validators

```js
db.runCommand({
  collMod: "products",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "category", "price", "stock"],
      properties: {
        price:    { bsonType: ["double", "decimal"], minimum: 0 },
        stock:    { bsonType: "int", minimum: 0 },
        category: { enum: ["smartphone", "laptop", "tablet", "audio", "wearable", "accessory", "desktop"] }
      }
    }
  },
  validationLevel: "moderate"
});
```

```js
db.products.insertOne({ _id: 12, name: "Bad Product", category: "smartphone", price: -50, stock: 10 });
// Document failed validation — price: -50 violates "minimum: 0"
```

Same fix as [Lesson 2.13](../02-sql/13-constraints.md)'s retroactive
`ALTER TABLE ... ADD CONSTRAINT` — `collMod` adds validation to a collection
that already exists, closing the exact same "nothing stops a negative price"
gap MongoDB's `products` collection has had since
[Lesson 3.2](02-your-first-database-apple-example.md).

`enum` here also functions as a `CHECK (category IN (...))` equivalent —
restricting `category` to a fixed, known list.

`validationLevel: "moderate"` means existing documents that don't already
satisfy the rule are left alone, but any *update* to them (and every new
insert) must comply — a gentler rollout than `"strict"`, which validates
every write against every document unconditionally.

## Step 5 — `NOT NULL`, and the `DEFAULT` gap

`required: [...]` above is the `NOT NULL` equivalent — those fields must be
present. But note what's **missing** compared to
[Lesson 2.13](../02-sql/13-constraints.md): there's no MongoDB equivalent of
SQL's `DEFAULT`. A field with no default fills in at the database level in
PostgreSQL; in MongoDB, *your application code* has to supply every field's
value at insert time (exactly what [Lesson 3.2](02-your-first-database-apple-example.md)
did manually with `created_at: new Date()`).

## Step 6 — Recap

| SQL ([Lesson 2.13](../02-sql/13-constraints.md)) | MongoDB |
|---|---|
| `PRIMARY KEY` | `_id`, unique automatically |
| `FOREIGN KEY` | **No equivalent** — not enforced (Lesson 3.10) |
| `UNIQUE` | `createIndex({ field: 1 }, { unique: true })` |
| `CHECK` | `$jsonSchema` validator (`minimum`, `maximum`, `enum`, ...) |
| `NOT NULL` | `required: [...]` in the validator |
| `DEFAULT` | **No equivalent** — the application must supply every value |
| Composite `PRIMARY KEY` | A compound unique index across multiple fields |

---
← [3.12 Aggregation Pipelines](12-aggregation-pipelines.md) | Next: [3.14 Transactions →](14-transactions.md)
