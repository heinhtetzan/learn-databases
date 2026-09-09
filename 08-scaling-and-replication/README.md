# Module 08 — Scaling & Replication

Eventually one machine isn't enough — either it can't hold all the data, or it
can't handle all the traffic. This module covers how databases grow past a
single machine: replication for reliability and read scaling, sharding for write
scaling, and the fundamental tradeoff (CAP theorem) that governs both.

## Lessons

1. [Replication](01-replication.md)
2. [Sharding & Partitioning](02-sharding-partitioning.md)
3. [The CAP Theorem](03-cap-theorem.md)

## Learning goals

By the end of this module you can:
- Explain the three main replication topologies and their tradeoffs
- Explain sharding, choose a reasonable shard key, and describe cross-shard query problems
- State the CAP theorem correctly and use it to reason about a system's design

---
[← Module 07](../07-nosql/) | [Course Home](../README.md) | Next: [Replication →](01-replication.md)
