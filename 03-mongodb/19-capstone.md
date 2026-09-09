← [3.18 User & Access Management](18-user-access-management.md)

# 3.19 Capstone: Product Reviews

The exact same feature as [Lesson 2.19](../02-sql/19-capstone.md) — product
reviews — rebuilt with everything from Part 2.

## Step 1 — Design: embed, or reference?

Applying [Lesson 3.9](09-embedding-vs-referencing.md)'s decision rule:
reviews are **not** bounded (a popular product could have thousands) and are
often queried **independently** of a specific product (e.g., "show all of
Alice's reviews"). Both point the same direction as
[Lesson 2.9](../02-sql/09-normalization.md)'s SQL design: a **separate**
`reviews` collection, referencing `customer_id` and `product_id` — not
embedded into `products`.

## Step 2 — Build the collection (Schema Validation)

```js
db.createCollection("reviews", {
  validator: {
    $jsonSchema: {
      required: ["customer_id", "product_id", "rating"],
      properties: {
        rating:  { bsonType: "int", minimum: 1, maximum: 5 },
        comment: { bsonType: "string" }
      }
    }
  }
});

db.reviews.createIndex({ customer_id: 1, product_id: 1 }, { unique: true });   // one review per customer per product
```

## Step 3 — Add reviews, as a transaction (Transactions)

Mirroring [Lesson 2.19](../02-sql/19-capstone.md)'s imagined
`review_count` sync:

```js
const session = db.getMongo().startSession();
session.startTransaction();
try {
  db.reviews.insertMany([
    { customer_id: 1, product_id: 1, rating: 5, comment: "Best phone I have owned." },
    { customer_id: 1, product_id: 7, rating: 4, comment: "Great sound, a bit pricey." },
    { customer_id: 2, product_id: 2, rating: 5, comment: "Perfect for travel." },
    { customer_id: 3, product_id: 4, rating: 3, comment: "Good, but battery could be better." }
  ], { session });
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

## Step 4 — Add the index (Indexes & Performance)

Already added in Step 2 — `{ customer_id: 1, product_id: 1 }` serves both as
the uniqueness guarantee *and* the index [Lesson 3.15](15-indexes-and-performance.md)
would otherwise ask you to add manually for `product_id` lookups.

## Step 5 — Per-product ratings (`$lookup` + `$group`)

```js
db.products.aggregate([
  { $lookup: { from: "reviews", localField: "_id", foreignField: "product_id", as: "productReviews" } },
  { $project: {
      name: 1,
      num_reviews: { $size: "$productReviews" },
      avg_rating: { $avg: "$productReviews.rating" }
  }},
  { $sort: { avg_rating: -1 } }
]);
```
| name | num_reviews | avg_rating |
|---|---|---|
| iPhone 17 Pro | 1 | 5.00 |
| MacBook Air | 1 | 5.00 |
| AirPods Max | 1 | 4.00 |
| iPad Air | 1 | 3.00 |
| MacBook Pro | 0 | `null` |
| iPad Pro | 0 | `null` |
| Mac Mini | 0 | `null` |
| iPhone 17 | 0 | `null` |

`$avg` on an empty array returns `null` automatically — no `NULLS LAST`
equivalent needed here since we're not sorting by it in this example, but
the same `$sort` + explicit `null`-handling approach from earlier lessons
would apply if you did.

## Step 6 — Save it as a view (Views)

```js
db.createView("product_ratings", "products", [
  { $lookup: { from: "reviews", localField: "_id", foreignField: "product_id", as: "productReviews" } },
  { $project: { name: 1, num_reviews: { $size: "$productReviews" }, avg_rating: { $avg: "$productReviews.rating" } } }
]);
```

## Step 7 — The final synthesis query — and an honest limit

*"Which products are outperforming average on **both** revenue and
rating?"* In SQL ([Lesson 2.19](../02-sql/19-capstone.md)), this was one
clean CTE-based query. In MongoDB, it genuinely takes more machinery —
worth seeing in full, not glossed over:

```js
db.products.aggregate([
  // 1. Revenue per product, from embedded order items across ALL orders
  { $lookup: {
      from: "orders", let: { pid: "$_id" },
      pipeline: [
        { $unwind: "$items" },
        { $match: { $expr: { $eq: ["$items.product_id", "$$pid"] } } },
        { $group: { _id: null, revenue: { $sum: { $multiply: ["$items.quantity", "$items.unit_price"] } } } }
      ],
      as: "revenueData"
  }},
  // 2. Rating per product
  { $lookup: { from: "reviews", localField: "_id", foreignField: "product_id", as: "productReviews" } },
  { $addFields: {
      revenue: { $ifNull: [{ $arrayElemAt: ["$revenueData.revenue", 0] }, 0] },
      avgRating: { $avg: "$productReviews.rating" }
  }},
  { $project: { name: 1, revenue: 1, avgRating: 1 } },
  // 3. Compute both overall averages AND keep the per-product list, side by side
  { $facet: {
      products: [{ $match: {} }],
      overallAvgRevenue: [{ $group: { _id: null, avg: { $avg: "$revenue" } } }],
      overallAvgRating:  [{ $match: { avgRating: { $ne: null } } }, { $group: { _id: null, avg: { $avg: "$avgRating" } } }]
  }},
  // 4. Filter the product list against both thresholds
  { $project: {
      result: { $filter: {
          input: "$products", as: "p",
          cond: { $and: [
              { $gt: ["$$p.revenue",   { $arrayElemAt: ["$overallAvgRevenue.avg", 0] }] },
              { $gt: ["$$p.avgRating", { $arrayElemAt: ["$overallAvgRating.avg", 0] }] }
          ]}
      }}
  }}
]);
```
```
{ result: [
  { name: "iPhone 17 Pro", revenue: 1249.00, avgRating: 5.00 },
  { name: "MacBook Air",   revenue: 989.10,  avgRating: 5.00 }
] }
```

**Identical result to SQL** — but notice what it took: 2 correlated
sub-pipeline `$lookup`s, a `$facet` to compute two overall averages
alongside the per-product data, and a final `$filter` to bring it together.
This is the same honest tradeoff from [Lesson 3.11](11-lookup-joins.md):
MongoDB handles "fetch one document with everything it needs" beautifully;
cross-document analytical questions like this one lean on more, and more
advanced, pipeline machinery than SQL's equivalent CTE.

## Step 8 — One last access-control touch

```js
db.grantRolesToUser("app_user", [
  { role: "orderProcessor", db: "apple_store" }   // from Lesson 3.18
]);
db.createRole({
  role: "reviewWriter",
  privileges: [{ resource: { db: "apple_store", collection: "reviews" }, actions: ["find", "insert"] }],
  roles: []
});
db.grantRolesToUser("app_user", ["reviewWriter"]);
```

No `update`/`remove` granted — reviews are immutable once posted, same rule
as [Lesson 2.19](../02-sql/19-capstone.md).

---
← [3.18 User & Access Management](18-user-access-management.md) | Next: [3.20 Part 2 Conclusion →](20-conclusion.md)
