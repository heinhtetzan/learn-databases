← [4.2 The Same Query, Two Ways](02-same-query-two-ways.md)

# 4.3 Pros and Cons

Everything below is grounded in something you actually built in Parts 1–2 —
not abstract claims.

## Data integrity

| | SQL | MongoDB |
|---|---|---|
| Foreign keys enforced? | Yes ([Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)) | **No** ([Lesson 3.10](../03-mongodb/10-relationships-in-mongodb.md)) |
| Type/shape rules enforced? | Yes, always (column types) | Only if you add `$jsonSchema` validation ([Lesson 3.13](../03-mongodb/13-schema-validation.md)) |
| `DEFAULT` values | Server-enforced | **No equivalent** — the app must supply every value |
| **Verdict** | Stronger guarantees, by default | Guarantees are opt-in, and some (FK) aren't available at all |

## Schema flexibility

| | SQL | MongoDB |
|---|---|---|
| Adding a new field | `ALTER TABLE`, affects every row | Just start writing it — no migration |
| Different records, different shapes | Awkward (nullable columns, or EAV anti-patterns) | Natural — every document can differ |
| **Verdict** | Rigid, in exchange for the guarantees above | Flexible, in exchange for those guarantees |

## Relationships and querying across data

| | SQL | MongoDB |
|---|---|---|
| Fetch one entity + its immediate details | `JOIN` | Often a single document read (if embedded) |
| Aggregate across many related records | `JOIN` + `GROUP BY`, one pass ([Lesson 2.11](../02-sql/11-joins.md)) | `$lookup` + `$reduce`/`$map`, more steps ([Lesson 3.11](../03-mongodb/11-lookup-joins.md)) |
| Recursive/hierarchical data | `WITH RECURSIVE` | `$graphLookup` — both handle it, similar effort |
| **Verdict** | Better at cross-record questions | Better at "fetch one whole thing" questions |

## Transactions

| | SQL | MongoDB |
|---|---|---|
| Single-row/document write | Atomic | Atomic |
| Multi-row/document write | Full transaction support, with `SAVEPOINT` | Full transaction support, **no** `SAVEPOINT` ([Lesson 3.14](../03-mongodb/14-transactions.md)) |
| **Verdict** | Slightly more complete transaction toolkit | Comparable for the common case; embedding often avoids needing one at all |

## Scaling

| | SQL | MongoDB |
|---|---|---|
| Vertical scaling (bigger machine) | Standard, well-understood | Standard, well-understood |
| Horizontal scaling (sharding) | Possible, but historically harder to bolt on | Built in from the start, generally simpler to configure |
| **Verdict** | Fine until very large scale | Built with horizontal scale as a first-class goal |

## Tooling and ecosystem

| | SQL | MongoDB |
|---|---|---|
| Language standardization | SQL is broadly similar across PostgreSQL/MySQL/SQL Server/Oracle ([Lesson 2.1](../02-sql/01-what-is-sql.md)) | Query syntax is MongoDB-specific — no equivalent "same skill, 4 brands" |
| Maturity | Decades of tooling, BI integrations, ORMs | Mature, but a younger ecosystem overall |
| **Verdict** | More transferable skill; more third-party tooling | Catching up fast, especially for JS/JSON-native stacks |

## The honest summary

Neither column wins outright. SQL trades flexibility for guarantees and
strong cross-record querying; MongoDB trades some guarantees and querying
complexity for flexibility and natural "fetch-one-thing" performance. Which
tradeoff is *right* depends entirely on what you're building —
[Lesson 4.4](04-real-world-scenarios.md) works through specific cases.

---
← [4.2 The Same Query, Two Ways](02-same-query-two-ways.md) | Next: [4.4 Real-World Scenarios & Which Fits →](04-real-world-scenarios.md)
