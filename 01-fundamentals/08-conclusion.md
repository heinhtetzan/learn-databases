← [1.7 Connecting with a GUI](07-gui-tools.md)

# 1.8 Module 1 Conclusion

Before jumping into Part 1, let's connect everything Module 1 actually
covered — and confirm you're genuinely ready to start writing real SQL.

## What you've learned

| Lesson | Big idea |
|---|---|
| [1.1 What Is Data?](01-what-is-data.md) | Data = raw facts; a database's job is to turn it back into usable information |
| [1.2 Structured Data & Storage Evolution](02-structured-data-and-storage-evolution.md) | Paper → spreadsheets → databases, each stage fixing the last one's specific problem |
| [1.3 Types of Databases](03-types-of-databases.md) | Relational, key-value, document, column-family, graph, vector — 6 shapes for 6 different needs |
| [1.4 Database Brands](04-database-brands.md) | PostgreSQL and MongoDB — this course's two chosen tools, and why |
| [1.5 Installing PostgreSQL & MongoDB](05-installation.md) | Getting both running natively, on any OS |
| [1.6 Running with Docker](06-run-with-docker.md) | The same two databases, containerized, with data persisted to your own folder |
| [1.7 Connecting with a GUI](07-gui-tools.md) | TablePlus and MongoDB Compass — seeing and editing your data visually |

## The one idea to carry forward

Every lesson in this module answered a version of the same question: *"how
do we store facts reliably, and get them back out again, precisely?"* Paper
ledgers, spreadsheets, and finally databases were all attempts at that same
goal — each one better than the last at handling scale, safety, and
precision. Everything in Part 1 (SQL) and Part 2 (MongoDB) is just a deeper,
more powerful answer to that exact same question.

## Readiness checklist

- [ ] I can explain the difference between data and information
- [ ] I can name at least 3 types of databases and when you'd pick each
- [ ] PostgreSQL is installed and running (natively or via Docker)
- [ ] I can connect to it with `psql` or TablePlus
- [ ] *(Optional for now)* MongoDB is installed, and Compass connects to it

If every box above is checked, you're ready. If PostgreSQL isn't running
yet, go back to [Lesson 1.5](05-installation.md) or
[Lesson 1.6](06-run-with-docker.md) before continuing — every lesson in Part
1 assumes a real, running database you can type queries into.

## What's next

**Part 1 — SQL** starts now: 17 lessons, building one real,
multi-table PostgreSQL database from scratch — from `SELECT` to joins,
transactions, and a final capstone. **Part 2 — NoSQL** picks up
afterward with MongoDB, applying the same ideas to a very different kind of
database.

---
← [1.7 Connecting with a GUI](07-gui-tools.md) | Next: [2.1 What Is SQL? →](../02-sql/01-what-is-sql.md)
