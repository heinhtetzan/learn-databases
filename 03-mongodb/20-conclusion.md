← [3.19 Capstone](19-capstone.md)

# 3.20 Part 2 Conclusion

Part 2 is done. Same data, same feature, same capstone — rebuilt entirely
with MongoDB's tools instead of PostgreSQL's.

## What you've learned

| Lesson | Big idea |
|---|---|
| [3.1 What Is MongoDB?](01-what-is-mongodb.md) | Documents in collections, not rows in tables — no separate query language layer |
| [3.2 Your First Database](02-your-first-database-apple-example.md) | `insertOne`/`insertMany`/`find`/`updateOne`/`deleteOne` — same data as Part 1's end-state |
| [3.3 Types of MongoDB Operations](03-types-of-mongodb-operations.md) | The same 5 SQL categories, mapped to MongoDB's own tools |
| [3.4 Data Types (BSON)](04-data-types.md) | `Decimal128` vs. `Double`, `ObjectId`, native nesting |
| [3.5 Query Operators](05-query-operators.md) | `$gt`, `$in`, `$regex`, `$exists`, `$and`/`$or` |
| [3.6 Sort, Limit, Skip](06-sort-limit-skip.md) | `.sort()`, `.limit()`, `.skip()` |
| [3.7 Aggregation Functions](07-aggregation-functions.md) | `$sum`/`$avg`/`$round`/`$toUpper`/`$ifNull`, inside a pipeline |
| [3.8 The `$group` Stage](08-group-stage.md) | Per-category summaries, `$match` before *and* after |
| [3.9 Embedding vs. Referencing](09-embedding-vs-referencing.md) | The central MongoDB design decision — and how it avoids (or reintroduces) SQL's anomalies |
| [3.10 Relationships in MongoDB](10-relationships-in-mongodb.md) | References, with **no enforcement** — a genuine, honest tradeoff |
| [3.11 `$lookup`](11-lookup-joins.md) | Joining collections — and the real cost of aggregating across embedded arrays |
| [3.12 Aggregation Pipelines](12-aggregation-pipelines.md) | `$facet`, `$graphLookup` — MongoDB's CTEs and recursive queries |
| [3.13 Schema Validation](13-schema-validation.md) | `$jsonSchema`, unique indexes — and what has no equivalent (`DEFAULT`, foreign keys) |
| [3.14 Transactions](14-transactions.md) | Single documents are atomic for free; multi-document needs a session — with no `SAVEPOINT` |
| [3.15 Indexes & Performance](15-indexes-and-performance.md) | The exact same B-Tree structure as PostgreSQL |
| [3.16 Views](16-views.md) | Saved pipelines, always read-only |
| [3.17 Create Collections: More Examples](17-create-collections-examples.md) | Capped collections and TTL indexes — genuinely MongoDB-only tools |
| [3.18 User & Access Management](18-user-access-management.md) | Roles and custom privileges, mirroring `GRANT`/`REVOKE` |
| [3.19 Capstone](19-capstone.md) | The identical feature, built with MongoDB's tools — same final answer, different path |

## The one idea to carry forward

Every SQL guarantee from Part 1 — enforced relationships, `DEFAULT` values,
partial rollback via `SAVEPOINT` — had to be **deliberately rebuilt, weakened,
or explicitly given up** somewhere in Part 2. That's not a flaw in MongoDB;
it's the actual trade being made: less enforced structure, in exchange for
flexibility and documents that map naturally onto how an application already
thinks about its data. Neither database is "better" in the abstract — they
made different bets, on purpose.

## Readiness checklist

- [ ] I can decide whether to embed or reference a given relationship, and explain why
- [ ] I can write a multi-stage aggregation pipeline with `$match`, `$group`, and `$lookup`
- [ ] I know exactly which SQL guarantees MongoDB does *not* enforce automatically
- [ ] I can start, commit, and abort a multi-document transaction
- [ ] I can create a role with only the collections/actions it actually needs

## What's next

[**Chapter 4**](../04-comparison/) puts both parts side by side directly —
the same data, the same queries, a structured pros-and-cons comparison, and
a practical framework for choosing between them on a real project.

---
← [3.19 Capstone](19-capstone.md) | Next: [Chapter 4 — Comparison →](../04-comparison/01-same-data-two-ways.md)
