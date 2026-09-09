# Module 05 — Indexing & Performance

A correct schema isn't enough at scale — you also need queries that stay fast as
data grows from thousands to millions of rows. This module opens up the "how" of
query execution and gives you a practical tuning workflow.

## Lessons

1. [Indexes Explained](01-indexes-explained.md)
2. [Reading Execution Plans](02-execution-plans.md)
3. [Performance Tuning in Practice](03-performance-tuning.md)

## Learning goals

By the end of this module you can:
- Explain how a B-tree index makes lookups fast, and when an index *won't* help
- Read `EXPLAIN`/`EXPLAIN ANALYZE` output to find out what a query is actually doing
- Diagnose and fix the most common real-world slow-query causes

---
[← Module 04](../04-schema-design/) | [Course Home](../README.md) | Next: [Indexes Explained →](01-indexes-explained.md)
