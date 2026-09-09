← [3.9 Embedding vs. Referencing](09-embedding-vs-referencing.md)

# 3.10 Relationships in MongoDB

[Lesson 3.9](09-embedding-vs-referencing.md) decided *what* to embed and
what to reference. Let's actually build it — and confront MongoDB's biggest
honest tradeoff versus [Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)'s
SQL foreign keys.

## Step 1 — One-to-many: `customers` → `orders`

```js
db.customers.insertMany([
  { _id: 1, name: "Alice Chen", email: "alice@mail.com", city: "New York" },
  { _id: 2, name: "Bob Diaz",   email: "bob@mail.com",   city: "Los Angeles" },
  { _id: 3, name: "Carla Ruiz", email: "carla@mail.com", city: "Chicago" }
]);

db.orders.insertMany([
  { _id: 1, customer_id: 1, order_date: ISODate("2026-03-01"),
    items: [ { product_id: 1, quantity: 1, unit_price: 1249.00 },
             { product_id: 7, quantity: 1, unit_price: 549.00 } ] },
  { _id: 2, customer_id: 2, order_date: ISODate("2026-03-02"),
    items: [ { product_id: 2, quantity: 1, unit_price: 989.10 } ] },
  { _id: 3, customer_id: 1, order_date: ISODate("2026-03-05"),
    items: [ { product_id: 5, quantity: 1, unit_price: 999.00 },
             { product_id: 10, quantity: 1, unit_price: 599.00 } ] }
]);
```

Same 3 orders as [Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)
— Alice has orders 1 and 3, Bob has order 2, and Carla has **zero orders**.

## Step 2 — No junction table needed here

[Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)'s many-to-many
between `orders` and `products` needed a separate `order_items` table.
Here, that relationship is already handled — it's embedded directly as each
order's `items` array, decided back in [Lesson 3.9](09-embedding-vs-referencing.md).
A genuine many-to-many that *does* need real references on both sides (e.g.,
products tagged with multiple categories, where tags are shared and queried
independently) would instead store an array of IDs: `tags: [3, 7, 12]`.

## Step 3 — The big honest difference: no enforcement

```js
db.orders.insertOne({
  _id: 99,
  customer_id: 9999,     // this customer does not exist
  order_date: ISODate("2026-03-10"),
  items: []
});
// Succeeds. No error. MongoDB has no idea customer_id 9999 doesn't exist.
```

Compare this to [Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md),
Step 5 — PostgreSQL's foreign key **rejected** exactly this. MongoDB has
**no equivalent mechanism**: a reference is just a plain number sitting in a
field, and nothing checks it points anywhere real.

```js
db.customers.deleteOne({ _id: 1 });   // Alice
// Succeeds too — even though orders 1 and 3 still reference customer_id: 1.
```

Same story — deleting a "still-referenced" customer is silently allowed. Run
`db.orders.deleteOne({ _id: 99 })` and `db.customers.insertOne({ _id: 1, ... })`
to undo the damage from this section before continuing.

## Step 4 — Living with that tradeoff

Since the database won't catch this for you, the responsibility shifts
entirely to your application:

- **Application-level checks** — look up the customer before inserting the
  order, in your own code.
- **Schema validation** ([Lesson 3.13](13-schema-validation.md)) — can
  enforce a field's *type* and *shape*, but not that its value exists in
  another collection.
- **Accept it, deliberately** — some teams choose MongoDB precisely for
  workloads where this risk is low (data rarely deleted, or eventual
  cleanup jobs are acceptable) and the flexibility is worth it.

This is a genuine, real cost of choosing MongoDB for relational-shaped data
— not a gap this course glosses over. [Chapter 4](../04-comparison/) weighs
it directly against SQL's guarantees.

## Step 5 — Recap

| | SQL ([Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)) | MongoDB |
|---|---|---|
| One-to-many | FK on the "many" side, enforced | Reference field, **not enforced** |
| Many-to-many | Junction table, enforced both sides | Array of IDs, **not enforced** |
| Insert with a bad reference | Rejected with an error | Silently succeeds |
| Delete a still-referenced row | Rejected by default (`RESTRICT`) | Silently succeeds |
| Who enforces correctness? | The database | Your application code |

---
← [3.9 Embedding vs. Referencing](09-embedding-vs-referencing.md) | Next: [3.11 `$lookup` (Joining Collections) →](11-lookup-joins.md)
