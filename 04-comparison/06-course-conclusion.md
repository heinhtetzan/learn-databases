← [4.5 Decision Framework](05-decision-framework.md)

# 4.6 Course Conclusion

You've built one real system — Apple's product/order data — twice, in two
fundamentally different databases, and then compared them directly, line by
line. That's the whole course. Here's the full shape of it.

## The whole course, at a glance

| Module | Focus | Detailed recap |
|---|---|---|
| **Module 1** | Fundamentals — what data is, database types, brands, setup | [1.8 Module 1 Conclusion](../01-fundamentals/08-conclusion.md) |
| **Part 1** | SQL, with PostgreSQL — 20 lessons, a full multi-table system | [2.20 Part 1 Conclusion](../02-sql/20-conclusion.md) |
| **Part 2** | NoSQL, with MongoDB — the same system, rebuilt | [3.20 Part 2 Conclusion](../03-mongodb/20-conclusion.md) |
| **Chapter 4** | Direct comparison, pros/cons, and how to decide | This module |

## The one idea underneath everything

Every module answered a version of the same question, from a different
angle: *"how do you store related facts, reliably, and get them back out
again, precisely?"* [Module 1](../01-fundamentals/01-what-is-data.md) asked
it in the abstract. Part 1 answered it with **enforced structure**. Part 2
answered it with **flexible structure, chosen deliberately**. Chapter 4
showed neither answer is universally correct — the right one depends on
what you're actually building, and real systems often need both answers at
once.

## What you can do now

- Design a normalized relational schema from a plain-English requirement,
  and know exactly when to deliberately denormalize.
- Write real SQL — filtering, sorting, joins, subqueries, transactions,
  indexes — not just recognize the keywords.
- Model the same data as MongoDB documents, and explain *why* you'd embed
  one relationship and reference another.
- Write MongoDB aggregation pipelines, including the genuinely harder
  cross-document cases.
- Look at a new project's requirements and make — and justify — a real
  SQL-vs-NoSQL decision, including "use both."

## Where to go from here

- **Build something real.** Apply this to your own project — that's where
  the remaining gaps in understanding actually surface.
- **Go deeper on one database.** PostgreSQL and MongoDB both have excellent
  official documentation covering far more than an intro course can —
  replication, advanced indexing, full-text search, and more.
- **Explore the database types this course only introduced**
  ([Lesson 1.3](../01-fundamentals/03-types-of-databases.md)) — key-value
  stores like Redis, graph databases like Neo4j, and vector databases for
  AI applications each solve a different shape of problem.
- **Revisit Chapter 4** whenever you're starting something new — the
  questions in [Lesson 4.5](05-decision-framework.md) age well.

Thanks for building this all the way through — from "what is data?" to a
real, working, twice-built system. That's not a small thing.

---
← [4.5 Decision Framework](05-decision-framework.md) | [Back to Course Home](../README.md)
