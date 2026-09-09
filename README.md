# Learn Databases

A hands-on, self-paced course from "what is a database?" to designing,
querying, and running real systems in both a relational database
(PostgreSQL) and a document database (MongoDB) — then comparing them
directly, on one real dataset built and rebuilt across both.

## How the course is organized

Each numbered folder is a **module**. Inside, numbered `.md` files are
**lessons** — read them in order. Every module ends with its own conclusion
lesson summarizing everything in it. Diagrams are embedded directly as
[Mermaid](https://mermaid.js.org/) charts (render automatically on GitHub,
VS Code, and most Markdown viewers), plus rendered PNG charts in
[`assets/images/`](assets/images/) for the ones worth a real illustration.

## Course map

| Module | Lessons | Topic |
|---|---|---|
| [01 — Fundamentals](01-fundamentals/) | 8 | What data is, database types, brands, installation (native + Docker), GUI tools |
| [02 — SQL (PostgreSQL)](02-sql/) | 20 | A full relational system: CRUD, joins, normalization, transactions, indexes, users, capstone |
| [03 — NoSQL (MongoDB)](03-mongodb/) | 20 | The exact same system, rebuilt as documents: embedding, `$lookup`, pipelines, capstone |
| [04 — Comparison](04-comparison/) | 6 | Same data and queries side by side, pros/cons, real-world scenarios, decision framework |

54 lessons in total. Start at [Module 1, Lesson 1](01-fundamentals/01-what-is-data.md)
and follow the "Next →" link at the bottom of each page straight through to
the end.

## The running example

Every lesson in Modules 2–4 uses the **same dataset** — an Apple Store's
products, customers, orders, and reviews — built up progressively and kept
100% consistent across both databases. That's deliberate: it means every
SQL-vs-MongoDB comparison in Module 4 is a real, checkable comparison, not
an abstract one.

## Prerequisites

- No programming or database experience needed to start Module 1.
- [Lesson 1.5](01-fundamentals/05-installation.md) and
  [Lesson 1.6](01-fundamentals/06-run-with-docker.md) walk through getting
  PostgreSQL and MongoDB actually running, natively or via Docker, before
  Module 2 begins.

## License

Provided for personal learning. Feel free to adapt it for teaching,
attribution appreciated.

---
Start: [Module 1 — Fundamentals →](01-fundamentals/01-what-is-data.md)
