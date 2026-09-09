← [Module 03](README.md) | [Course Home](../README.md)

# 3.2 DML & CRUD

**DML (Data Manipulation Language)** reads and writes the rows inside tables:
`INSERT`, `SELECT`, `UPDATE`, `DELETE` — commonly abbreviated **CRUD** (Create,
Read, Update, Delete).

## Create: `INSERT`

```sql
INSERT INTO authors (author_id, name, country)
VALUES (1, 'Ursula K. Le Guin', 'USA');

-- Insert multiple rows at once
INSERT INTO authors (author_id, name, country) VALUES
    (2, 'Haruki Murakami', 'Japan'),
    (3, 'Chimamanda Ngozi Adichie', 'Nigeria');
```

If a column has a `DEFAULT` or allows `NULL`, you can omit it:

```sql
INSERT INTO books (book_id, title, author_id, genre, price, published)
VALUES (1, 'The Left Hand of Darkness', 1, 'Science Fiction', 12.99, '1969-03-01');
-- stock defaults to 0, as defined in the schema
```

## Read: `SELECT`

```sql
SELECT * FROM books;                      -- every column
SELECT title, price FROM books;           -- specific columns
SELECT title, price AS current_price      -- rename a column in the output
FROM books;
```

`SELECT *` is convenient for exploring but avoid it in application code — it
breaks silently if columns are added/reordered, and it fetches data you may not
need. Name columns explicitly in real applications.

## Update: `UPDATE`

```sql
UPDATE books
SET price = 14.99
WHERE book_id = 1;

-- update multiple columns at once
UPDATE books
SET price = price * 1.1, stock = stock - 1
WHERE book_id = 1;
```

> ⚠️ **The most dangerous mistake in SQL**: forgetting the `WHERE` clause.
> `UPDATE books SET price = 14.99;` with no `WHERE` updates **every row in the
> table**. Always write and double-check the `WHERE` clause — many people write
> the matching `SELECT` first to preview which rows will be affected:
>
> ```sql
> -- Preview first:
> SELECT * FROM books WHERE book_id = 1;
> -- Then update with the exact same WHERE clause:
> UPDATE books SET price = 14.99 WHERE book_id = 1;
> ```

## Delete: `DELETE`

```sql
DELETE FROM order_items WHERE order_id = 5;
DELETE FROM orders WHERE order_id = 5;
```

Same warning applies: `DELETE FROM books;` with no `WHERE` deletes every row.
Note the **order** above — `order_items` is deleted before `orders` because a
foreign key (by default) prevents deleting an `orders` row that `order_items`
still references. (`ON DELETE CASCADE`, covered in
[Module 02, Lesson 2](../02-relational-model/02-keys-and-constraints.md), would
let you delete just the `orders` row and have `order_items` clean up
automatically — a design decision to make deliberately.)

## Returning affected rows (Postgres/SQLite)

```sql
DELETE FROM books WHERE stock = 0 RETURNING book_id, title;
```

Handy for confirming exactly what an `UPDATE`/`DELETE`/`INSERT` touched, in one
round trip, without a separate `SELECT`.

## Upsert: insert-or-update

A common real-world need: "insert this row, but if it already exists, update it
instead."

```sql
-- PostgreSQL / SQLite
INSERT INTO books (book_id, title, author_id, genre, price, published)
VALUES (1, 'The Left Hand of Darkness', 1, 'Science Fiction', 13.99, '1969-03-01')
ON CONFLICT (book_id)
DO UPDATE SET price = EXCLUDED.price;

-- MySQL
INSERT INTO books (book_id, title, author_id, genre, price, published)
VALUES (1, 'The Left Hand of Darkness', 1, 'Science Fiction', 13.99, '1969-03-01')
ON DUPLICATE KEY UPDATE price = VALUES(price);
```

## Transactions (a preview)

Multiple DML statements often need to succeed or fail **together** — e.g.,
placing an order means inserting into `orders` *and* `order_items` *and*
decrementing `stock`, and none of that should partially apply.

```sql
BEGIN;
INSERT INTO orders (order_id, customer_id, order_date) VALUES (10, 2, CURRENT_DATE);
INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES (10, 1, 2, 13.99);
UPDATE books SET stock = stock - 2 WHERE book_id = 1;
COMMIT;   -- or ROLLBACK; to undo everything since BEGIN
```

We cover exactly what guarantees `BEGIN`/`COMMIT`/`ROLLBACK` give you, and what
can still go wrong with concurrent transactions, in full in
[Module 06](../06-transactions-concurrency/01-acid.md).

## Try it yourself

Using the bookstore schema:
1. Insert 3 authors, 5 books (across at least 2 genres), and 2 customers.
2. Place one order for a customer containing 2 different books, updating `stock`
   accordingly — wrap it in a transaction.
3. Write an `UPDATE` that raises the price of every book in one genre by 10%,
   previewing the affected rows with a `SELECT` first.
4. Delete a book that has no orders against it (yet) — notice what happens if you
   try to delete one that *does* have an order referencing it.

---
← [3.1 DDL Basics](01-ddl-basics.md) | [Module 03](README.md) | Next: [Filtering & Sorting →](03-filtering-sorting.md)
