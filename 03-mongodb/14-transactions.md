← [3.13 Schema Validation](13-schema-validation.md)

# 3.14 Transactions

Same 3 scenarios as [Lesson 2.14](../02-sql/14-transactions.md) — a bank
transfer, an airline booking, a shop checkout — all needing several writes
to succeed together, or not at all.

## Step 1 — The good news first: single documents are already atomic

Because [Lesson 3.9](09-embedding-vs-referencing.md) embedded `items`
directly inside each order, **inserting one whole order — items and all —
is already a single, atomic write**, with no transaction needed at all. This
is a genuine MongoDB strength: a well-embedded document sidesteps the
multi-statement problem entirely for anything that fits in one document.

The remaining gap: giving Carla her first order still means **two separate
documents** changing together — inserting her order, *and* reducing
`products` stock. That still needs a real transaction.

## Step 2 — Starting a transaction

```js
const session = db.getMongo().startSession();
session.startTransaction();
try {
  // ... operations, each passed { session } ...
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

Every operation inside must explicitly pass `{ session }`, or it runs
**outside** the transaction entirely — an easy mistake with no error to warn
you, worth double-checking every time.

## Step 3 — A failed attempt, and what rolls back

```js
session.startTransaction();
try {
  db.orders.insertOne({
    _id: 4,
    customer_id: 3,
    order_date: ISODate("2026-03-10"),
    items: [ { product_id: 4, quantity: 2, unit_price: 599.00 } ]
  }, { session });

  db.products.updateOne(
    { _id: 4 },
    { $inc: { stock: -99999 } },   // way more than in stock
    { session }
  );

  session.commitTransaction();
} catch (e) {
  print("Transaction aborted:", e.message);
  // Document failed validation — stock would go negative,
  // violating Lesson 3.13's "minimum: 0" rule
  session.abortTransaction();
}
```

`abortTransaction()` undoes **both** operations — including the `orders`
insert that, on its own, would have succeeded. Same all-or-nothing guarantee
as [Lesson 2.14](../02-sql/14-transactions.md)'s `ROLLBACK`.

> Unlike SQL's `SERIAL` ([Lesson 2.14](../02-sql/14-transactions.md)),
> nothing here auto-consumed the value `4` — MongoDB has no sequence
> counting attempts behind the scenes. `_id: 4` is genuinely free to reuse.
> We'll skip to `5` anyway below, purely to keep matching
> [Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)'s order
> numbering for easy comparison.

## Step 4 — The corrected, successful transaction

```js
session.startTransaction();
try {
  db.orders.insertOne({
    _id: 5,
    customer_id: 3,   // Carla's first order
    order_date: ISODate("2026-03-10"),
    items: [ { product_id: 4, quantity: 2, unit_price: 599.00 } ]
  }, { session });

  db.products.updateOne(
    { _id: 4 },
    { $inc: { stock: -2 } },   // iPad Air: 400 → 398
    { session }
  );

  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

Carla finally has her first order — matching
[Lesson 2.14](../02-sql/14-transactions.md)'s SQL result exactly.

## Step 5 — Bob's second order

```js
session.startTransaction();
try {
  db.orders.insertOne({
    _id: 6,
    customer_id: 2,
    order_date: ISODate("2026-03-12"),
    items: [ { product_id: 3, quantity: 1, unit_price: 1799.10 } ]
  }, { session });

  db.products.updateOne({ _id: 3 }, { $inc: { stock: -1 } }, { session });

  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

## Step 6 — What's missing: no `SAVEPOINT`

[Lesson 2.14](../02-sql/14-transactions.md)'s `SAVEPOINT` let SQL undo
*part* of a transaction while keeping the rest. MongoDB has **no
equivalent** — a transaction is all-or-nothing with no partial rollback
point. If step 3 of a 5-step transaction fails, all 5 steps abort; there's
no way to keep steps 1–2 and only retry step 3.

## Step 7 — A preview: atomic single-document updates

```js
db.products.updateOne(
  { _id: 4, stock: { $gte: 2 } },
  { $inc: { stock: -2 } }
);
```

Same idea as [Lesson 2.14](../02-sql/14-transactions.md)'s
`UPDATE ... WHERE stock >= 2` — and since a single document's update is
*always* atomic in MongoDB, this needs no transaction at all: if two
requests race, only one can actually succeed in reducing stock below the
guard.

## Recap

| SQL ([Lesson 2.14](../02-sql/14-transactions.md)) | MongoDB |
|---|---|
| `BEGIN` | `session.startTransaction()` |
| `COMMIT` | `session.commitTransaction()` |
| `ROLLBACK` | `session.abortTransaction()` |
| `SAVEPOINT` | **No equivalent** — all-or-nothing only |
| Multi-statement atomicity | Needed for multi-*document* writes; a single document is already atomic |

---
← [3.13 Schema Validation](13-schema-validation.md) | Next: [3.15 Indexes & Performance →](15-indexes-and-performance.md)
