← [3.3 Types of MongoDB Operations](03-types-of-mongodb-operations.md)

# 3.4 Data Types in MongoDB (BSON)

MongoDB stores documents as **BSON** (Binary JSON) — JSON's familiar shape,
plus extra types JSON itself doesn't have (like real dates and dedicated
integer sizes).

## 3 real-world scenarios

**1. An online store's checkout** must never let `price` hold text — same
risk as [Lesson 2.4](../02-sql/04-postgresql-data-types.md)'s SQL example,
just enforced differently here (BSON types, not a rigid column type).

**2. A product's unique identifier** needs a value guaranteed unique across
every document ever inserted, even from different servers writing at once —
exactly what MongoDB's `ObjectId` type exists for.

**3. A product's specs** (`storage_gb`, `color`, `has_5g`) naturally belong
*inside* the product itself, not scattered across separate tables — nesting
is a first-class BSON capability, not a workaround.

## The core BSON types

| Type | Use for | Example value |
|---|---|---|
| `String` | Text | `"iPhone 17 Pro"` |
| `Int32` / `Int64` (`NumberLong`) | Whole numbers | `500` |
| `Double` | Approximate decimals (careful — see below) | `1249.0` |
| `Decimal128` | **Exact** decimals — use for money | `NumberDecimal("1249.00")` |
| `Boolean` | `true` / `false` | `true` |
| `Date` | Date + time | `new Date("2026-02-01")` |
| `ObjectId` | Globally unique auto-generated ID | `ObjectId("65f1a2b3c4d5e6f7a8b9c0d1")` |
| `Array` | A list of values in one field | `["red", "blue", "green"]` |
| `Object` (embedded document) | Nested data, right inside the document | `{ storage_gb: 256, color: "black" }` |
| `Null` | Explicitly no value | `null` |

## The one gotcha worth memorizing: `Double` vs. `Decimal128`

Just like [Lesson 2.4](../02-sql/04-postgresql-data-types.md)'s
`FLOAT` vs. `DECIMAL` warning, plain numbers in MongoDB (and JSON generally)
default to floating-point `Double` — which has the exact same rounding
problem:

```js
db.test.insertOne({ amount: 0.1 + 0.2 });
db.test.findOne().amount;
// 0.30000000000000004 — NOT exactly 0.3
```

For genuinely exact money values, use `Decimal128` explicitly:

```js
db.test.insertOne({ amount: NumberDecimal("0.1") });
```

In practice, many real MongoDB applications store money as **integer cents**
(`124900` instead of `1249.00`) specifically to sidestep this entirely —
worth knowing as a common, pragmatic alternative.

## `ObjectId`: MongoDB's default unique ID

If you don't provide `_id` yourself (like [Lesson 3.2](02-your-first-database-apple-example.md)
did with plain integers), MongoDB generates a 12-byte `ObjectId` —
guaranteed unique across collections, servers, and time, without needing a
central counter the way SQL's `SERIAL` does:

```js
db.reviews.insertOne({ product_id: 1, rating: 5 });
// _id is auto-assigned, e.g. ObjectId("65f1a2b3c4d5e6f7a8b9c0d1")
```

## Nesting: the capability SQL doesn't have

```js
{
  _id: 1,
  name: "iPhone 17 Pro",
  specs: { storage_gb: 256, color: "black", has_5g: true }
}
```

`specs` is an embedded document — no separate `product_specs` table needed.
[Lesson 3.9](09-embedding-vs-referencing.md) covers exactly when this is a
good idea, and when it isn't.

## Recap: BSON vs. PostgreSQL types

| Concept | PostgreSQL ([Lesson 2.4](../02-sql/04-postgresql-data-types.md)) | MongoDB |
|---|---|---|
| Text | `TEXT` | `String` |
| Whole number | `INTEGER` | `Int32`/`Int64` |
| Exact decimal | `DECIMAL(p,s)` | `Decimal128` |
| True/false | `BOOLEAN` | `Boolean` |
| Date + time | `TIMESTAMP` | `Date` |
| Auto-generated unique ID | `SERIAL` | `ObjectId` |
| List of values | `ARRAY` | `Array` |
| Nested structured data | `JSONB` | Native — every document can nest |

---
← [3.3 Types of MongoDB Operations](03-types-of-mongodb-operations.md) | Next: [3.5 Query Operators →](05-query-operators.md)
