# Module 06 — Transactions & Concurrency

What happens when two users hit the same data at the same instant? This module
covers the guarantees that keep your data correct under concurrent load — ACID,
isolation levels, and how databases implement them internally (locking and MVCC).

## Lessons

1. [ACID Explained](01-acid.md)
2. [Isolation Levels](02-isolation-levels.md)
3. [Locking & MVCC](03-locking-mvcc.md)

## Learning goals

By the end of this module you can:
- Explain each ACID guarantee with a concrete example of what breaks without it
- Name the classic concurrency anomalies and which isolation level prevents each
- Explain, at a high level, how locking and MVCC each solve concurrent access

---
[← Module 05](../05-indexing-performance/) | [Course Home](../README.md) | Next: [ACID Explained →](01-acid.md)
