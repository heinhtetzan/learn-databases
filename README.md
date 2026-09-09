# Learn Databases — A Complete Training Course

A hands-on, self-paced course that takes you from "what is a database?" to designing,
querying, tuning, and scaling real production systems — relational and NoSQL alike.

## Who this is for

Anyone comfortable using a computer who wants a solid, practical understanding of
databases: developers, analysts, QA engineers, or students. No prior database
experience is assumed. By the end, you'll be able to design a schema, write real SQL,
reason about performance and transactions, and know when (and when not) to reach for NoSQL.

## How the course is organized

Each numbered folder is a **module**. Inside, numbered `.md` files are **lessons** —
read them in order. Diagrams are embedded directly in the Markdown as
[Mermaid](https://mermaid.js.org/) charts (render automatically on GitHub, VS Code,
and most Markdown viewers) plus a few rendered PNG charts in [`assets/images/`](assets/images/).

Every lesson ends with a **"Try it yourself"** exercise. Do them — reading about SQL
and writing SQL are very different skills.

## Course map

| Module | Topic | You'll learn |
|---|---|---|
| [01 — Fundamentals](01-fundamentals/) | What databases are | Core concepts, database types, DBMS architecture |
| [02 — Relational Model](02-relational-model/) | Relational theory | Tables, keys, constraints, normalization |
| [03 — SQL Fundamentals](03-sql-fundamentals/) | Practical SQL | DDL, CRUD, filtering, joins, aggregation, subqueries/CTEs |
| [04 — Schema Design](04-schema-design/) | Modeling real systems | ER modeling, a full case study, anti-patterns |
| [05 — Indexing & Performance](05-indexing-performance/) | Making queries fast | Index internals, execution plans, tuning |
| [06 — Transactions & Concurrency](06-transactions-concurrency/) | Correctness under load | ACID, isolation levels, locking & MVCC |
| [07 — NoSQL](07-nosql/) | Beyond relational | Key-value, document, column-family, graph stores |
| [08 — Scaling & Replication](08-scaling-and-replication/) | Growing past one machine | Replication, sharding, CAP theorem |
| [09 — Security & Administration](09-security-and-administration/) | Running it safely | Access control, backup & recovery |
| [10 — Capstone Project](10-capstone-project/) | Putting it together | Design and build a full database from a real brief |

## Prerequisites

- Comfort with a command line is helpful but not required.
- No programming or SQL experience needed to start Module 1.
- For hands-on practice, install a free relational database — [PostgreSQL](https://www.postgresql.org/download/)
  is recommended — or use an online sandbox like [DB Fiddle](https://www.db-fiddle.com/).

## Suggested pace

- **Fast track** (SQL only, for developers who just need to query a DB): Modules 1–3.
- **Full course** (design + build + run production systems): all 10 modules, ~3–5 weeks
  at a lesson or two per day.

## License

This course is provided for personal learning. Feel free to adapt it for teaching,
attribution appreciated.

---
Next: [Module 1 — Fundamentals →](01-fundamentals/)
