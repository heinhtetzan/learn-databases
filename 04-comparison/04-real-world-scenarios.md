← [4.3 Pros and Cons](03-pros-and-cons.md)

# 4.4 Real-World Scenarios & Which Fits

7 real scenarios, each with a recommendation and the specific reasoning
behind it — using [Lesson 4.3](03-pros-and-cons.md)'s tradeoffs applied to
an actual situation.

## 1. A bank's core ledger

**Recommendation: SQL.** Every transfer must debit one account and credit
another together, with zero tolerance for a partial write or an orphaned
reference — exactly [Lesson 2.10](../02-sql/10-relationships-and-foreign-keys.md)'s
enforced foreign keys and [Lesson 2.14](../02-sql/14-transactions.md)'s
transaction guarantees, in the one domain where "the database enforces it,
not just the application" genuinely matters most.

## 2. An e-commerce product catalog

**Recommendation: MongoDB**, or a hybrid. A book has `author`/`ISBN`; a
laptop has `CPU`/`RAM`; a t-shirt has `size`/`color` — exactly
[Lesson 3.1](../03-mongodb/01-what-is-mongodb.md)'s opening scenario. Many
real e-commerce systems actually run **both**: MongoDB for the catalog,
SQL for orders/payments/inventory, since those need the stronger guarantees
from scenario 1.

## 3. A social media "who to follow" recommendation

**Recommendation: Neither, strictly** — a **graph database** ([Lesson 1.3](../01-fundamentals/03-types-of-databases.md))
fits best for deep relationship traversal. Between just SQL and MongoDB,
lean MongoDB: [Lesson 3.12](../03-mongodb/12-aggregation-pipelines.md)'s
`$graphLookup` handles multi-hop traversal more naturally than repeated SQL
self-joins.

## 4. IoT sensor data / application logs

**Recommendation: MongoDB.** Massive write volume, loosely structured
records, and — from [Lesson 3.17](../03-mongodb/17-create-collections-examples.md)
— **capped collections** and **TTL indexes** are purpose-built for exactly
this: high-volume data that should expire or self-limit automatically,
something SQL has no equivalent for at all.

## 5. A hospital's patient records

**Recommendation: SQL**, for the core record — enforced relationships
between patients/doctors/appointments matter for safety and legal
compliance ([Lesson 2.13](../02-sql/13-constraints.md)'s guaranteed data
integrity). Free-text clinical notes or varying lab-result formats
*attached* to a patient are a reasonable candidate for MongoDB, or a
`JSONB` column ([Lesson 2.4](../02-sql/04-postgresql-data-types.md)) inside
the same SQL database.

## 6. A mobile game's leaderboard and player profile

**Recommendation: MongoDB.** Player profiles evolve constantly (new
achievements, changing stat fields) exactly like
[Lesson 3.1](../03-mongodb/01-what-is-mongodb.md)'s scenario 3 — no
migration needed every time a new feature ships a new field.

## 7. A university's course enrollment system

**Recommendation: SQL.** Enrollment is fundamentally relational — students,
courses, and the many-to-many link between them, with hard rules ("can't
enroll in a cancelled course," "can't exceed course capacity") that
[Lesson 2.13](../02-sql/13-constraints.md)'s constraints enforce
automatically, and [Lesson 2.11](../02-sql/11-joins.md)'s joins query
naturally.

## The pattern across all 7

| Signal | Points toward |
|---|---|
| Strict rules that must never be violated, money/legal/safety involved | SQL |
| Data shape varies a lot between records | MongoDB |
| Deep, complex relationships queried constantly | SQL |
| Massive write volume, loosely structured, often time-limited | MongoDB |
| A big system with different needs in different places | **Both** — polyglot persistence, covered next |

---
← [4.3 Pros and Cons](03-pros-and-cons.md) | Next: [4.5 Decision Framework →](05-decision-framework.md)
