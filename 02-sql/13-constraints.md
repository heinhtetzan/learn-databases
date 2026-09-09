← [2.12 Subqueries & CTEs](12-subqueries-and-ctes.md)

# 2.13 Constraints

You've used `PRIMARY KEY`, `REFERENCES`, `UNIQUE`, `CHECK`, `NOT NULL`, and
`DEFAULT` informally since [Lesson 2.2](02-your-first-database-apple-example.md).
Let's formalize each one, and notice something we've been missing.

## Step 1 — `PRIMARY KEY`: uniquely identifies each row

```sql
product_id SERIAL PRIMARY KEY
```
Every table so far — `products`, `customers`, `orders` — uses this pattern.
A primary key must be unique across every row and can never be `NULL`.

## Step 2 — `FOREIGN KEY`: enforces valid relationships

```sql
customer_id INTEGER NOT NULL REFERENCES customers(customer_id)
```
Covered fully in [Lesson 2.10](10-relationships-and-foreign-keys.md) — every
value must already exist in the referenced table. You can also control what
happens if the referenced row is later *updated* (rare, but symmetric with
`ON DELETE`):

```sql
customer_id INTEGER REFERENCES customers(customer_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE   -- if a customer_id value ever changed, update it here too
```

## Step 3 — `UNIQUE`: no two rows share this value

```sql
email TEXT NOT NULL UNIQUE   -- from customers, Lesson 2.10
```

```sql
INSERT INTO customers (name, email, city) VALUES ('David Kim', 'alice@mail.com', 'Boston');
-- ERROR: duplicate key value violates unique constraint "customers_email_key"
-- Key (email)=(alice@mail.com) already exists.
```

Unlike `PRIMARY KEY`, a `UNIQUE` column *can* hold multiple `NULL`s (each
`NULL` is considered "unknown," never equal to another `NULL`) — but every
non-`NULL` value must be distinct.

## Step 4 — `CHECK`: a custom validation rule

```sql
quantity INTEGER NOT NULL CHECK (quantity > 0)   -- from order_items, Lesson 2.10
```

```sql
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (1, 4, -2, 599.00);
-- ERROR: new row for relation "order_items" violates check constraint "order_items_quantity_check"
```

## Step 5 — Wait — our `products` table is missing a `CHECK`

Look back at [Lesson 2.2](02-your-first-database-apple-example.md)'s
`CREATE TABLE products`: `price` and `stock` are `NOT NULL`, but **nothing
stops a negative value**. This has been a real gap since Lesson 2.2 — let's
fix it now with `ALTER TABLE`:

```sql
ALTER TABLE products ADD CONSTRAINT price_positive CHECK (price > 0);
ALTER TABLE products ADD CONSTRAINT stock_non_negative CHECK (stock >= 0);
```

```sql
UPDATE products SET price = -50 WHERE product_id = 1;
-- ERROR: new row for relation "products" violates check constraint "price_positive"
```

This is a good habit generally: constraints don't all need to be decided at
`CREATE TABLE` time — you can (and should) tighten a schema with `ALTER
TABLE` the moment you notice a gap, exactly like this.

## Step 6 — `NOT NULL` and `DEFAULT`, recapped

```sql
stock      INTEGER NOT NULL DEFAULT 0                     -- products, Lesson 2.2
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP    -- products, Lesson 2.2
order_date DATE NOT NULL DEFAULT CURRENT_DATE              -- orders, Lesson 2.10
```

- `NOT NULL` — this field must always have a value.
- `DEFAULT` — the value used automatically when none is given on `INSERT`.

## Step 7 — Composite primary keys

```sql
PRIMARY KEY (order_id, product_id)   -- order_items, Lesson 2.10
```

Neither `order_id` nor `product_id` is unique alone in `order_items` (an
order has many products; a product appears in many orders) — but the *pair*
together is. This also directly enforces a business rule: **a given order
can't list the same product twice** as two separate rows.

```sql
-- ❌ Rejected — (order_id=1, product_id=1) already exists
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (1, 1, 5, 1249.00);
-- ERROR: duplicate key value violates unique constraint "order_items_pkey"
```

## Step 8 — Recap

| Constraint | Enforces | Example from our schema |
|---|---|---|
| `PRIMARY KEY` | Unique row identity, never `NULL` | `product_id SERIAL PRIMARY KEY` |
| `FOREIGN KEY` / `REFERENCES` | Value must exist in another table | `customer_id REFERENCES customers(customer_id)` |
| `UNIQUE` | No duplicate values (NULLs excepted) | `email TEXT UNIQUE` |
| `CHECK` | Custom validation rule | `CHECK (price > 0)` |
| `NOT NULL` | Value can never be missing | `name TEXT NOT NULL` |
| `DEFAULT` | Auto-fill when no value given | `stock INTEGER DEFAULT 0` |
| Composite `PRIMARY KEY` | Uniqueness across a *combination* of columns | `PRIMARY KEY (order_id, product_id)` |

Every constraint here is a rule the **database itself** enforces — bugs in
application code simply can't violate them, which is exactly why they're
worth adding deliberately, not left to "we'll validate it in the app."

---
← [2.12 Subqueries & CTEs](12-subqueries-and-ctes.md) | Next: [2.14 Transactions →](14-transactions.md)
