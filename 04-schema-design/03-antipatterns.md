← [Module 04](README.md) | [Course Home](../README.md)

# 4.3 Schema Anti-Patterns

Mistakes experienced developers still make, why they hurt, and the fix for each.

## 1. The "one big table" anti-pattern

Cramming everything into a single flat table (see
[Module 02, Lesson 3](../02-relational-model/03-normalization.md) for the full
example) to "avoid joins." This reintroduces every update/insertion/deletion
anomaly normalization exists to prevent. **Fix**: normalize to at least 3NF,
then denormalize *specific* columns deliberately, only when you have a measured
performance reason.

## 2. Storing comma-separated lists in a column

```sql
-- ❌ Anti-pattern
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title   TEXT,
    tags    TEXT   -- "sci-fi,classic,award-winning"
);
```

This violates 1NF. You can't index individual tags, can't query "books tagged
`classic`" without fragile `LIKE '%classic%'` matching, and can't enforce tag
validity. **Fix**: a proper many-to-many junction table (`book_tags`), or — if
your database supports it — a native array/JSON column *specifically* when you
never need to query inside it relationally (e.g., Postgres `TEXT[]` or `JSONB`
for genuinely unstructured, rarely-queried metadata).

## 3. Entity-Attribute-Value (EAV) overuse

Trying to make a schema infinitely flexible by storing everything as generic
key-value rows:

```sql
-- ❌ Anti-pattern: "flexible" product attributes
CREATE TABLE product_attributes (
    product_id INTEGER,
    attr_name  TEXT,
    attr_value TEXT
);
```

This looks flexible but destroys type safety (`attr_value` is always text — no
`CHECK`, no numeric comparisons without casting), makes simple queries require
many self-joins, and the database can no longer enforce which attributes are
required. **Fix**: model the attributes you actually know about as real
columns; reach for a `JSONB` column (Postgres) only for the genuinely
unpredictable long tail, and only if you rarely need to query inside it. If
different product *types* have wildly different attributes, this is often a
sign you actually want a document database — see
[Module 07](../07-nosql/02-key-value-and-document-stores.md).

## 4. No foreign keys ("we'll enforce it in the app")

Skipping foreign key constraints for "flexibility" or perceived performance
means the database can no longer guarantee referential integrity — a bug in
*any* code path (a script, a migration, a rushed hotfix) can silently create
orphaned rows. **Fix**: always declare foreign keys. The performance cost is
negligible for the integrity you get; if you truly hit a case where FK checks
measurably matter, that's a decision to make with data, not by default.

## 5. Using `FLOAT`/`REAL` for money

```sql
-- ❌ Anti-pattern
price FLOAT
```

Floating point can't represent most decimal fractions exactly, leading to
values like `19.999999999998` after arithmetic. **Fix**: `DECIMAL(p,s)` /
`NUMERIC(p,s)` for any exact value — money, quantities that must reconcile
exactly, anything audited.

## 6. Generic, ambiguous names

Columns named `data`, `value`, `type`, `status`, `flag1` (or worse, tables named
`table1`, `temp`, `data2`) with no documentation. Six months later, nobody
remembers what `status = 3` means. **Fix**: name things for what they *are*
(`order_status`, not `status`); for a fixed set of meaningful values, use an
`ENUM` type or a `CHECK (status IN (...))` constraint or a lookup table — never
a bare "magic number."

## 7. Polymorphic associations without database-level enforcement

```sql
-- ❌ Anti-pattern: comments on "either a post or a photo"
CREATE TABLE comments (
    comment_id     INTEGER PRIMARY KEY,
    commentable_id INTEGER,      -- could be a post_id OR a photo_id
    commentable_type TEXT,       -- 'post' or 'photo' — decided by app code
    body           TEXT
);
```

The database has no way to enforce `commentable_id` actually exists in the
right table — no real foreign key is possible here. **Fix**: either use
separate tables (`post_comments`, `photo_comments`), or a shared parent table
(`commentable_items`) that both `posts` and `photos` reference, restoring real
foreign key integrity.

## 8. Premature/unjustified denormalization

The inverse mistake from #1: duplicating data "for performance" before you've
measured a real bottleneck, without a clear plan for keeping the copies in
sync. Every denormalized value is a promise that two places will always agree
— broken promises are subtle, hard-to-find bugs. **Fix**: normalize first;
denormalize only for a measured, specific hot path, and centralize the sync
logic (a trigger, a single write path, or a scheduled job) rather than trusting
every caller to remember.

## Quick reference: symptoms → likely anti-pattern

| Symptom you notice | Likely cause |
|---|---|
| "I have to update the same fact in 5 places" | Missing normalization (#1) |
| "I can't query for a specific tag/attribute efficiently" | CSV column or EAV (#2, #3) |
| "We have orphaned rows referencing deleted records" | Missing foreign keys (#4) |
| "Our totals don't reconcile with the sum of line items" | `FLOAT` for money (#5) |
| "New engineers keep asking what this column means" | Poor naming (#6) |
| "This join needs a `CASE` statement to know which table to hit" | Polymorphic association (#7) |
| "Our cache/copy of X keeps drifting from the real value" | Unmanaged denormalization (#8) |

## Try it yourself

Look back at the schema you designed in the previous lesson's exercise
(wishlists). Check it against this list — does it accidentally introduce any of
these anti-patterns? If you used a `JSONB`/array column anywhere, justify (in a
comment) why that specific case is an exception rather than an EAV mistake in
disguise.

---
← [4.2 Case Study: Bookstore Schema](02-case-study-bookstore.md) | [Module 04](README.md) | Next: [Module 05 — Indexing & Performance →](../05-indexing-performance/)
