← [2.17 Create Tables: More Examples](17-create-tables-examples.md)

# 2.18 User & Access Management

Before any code — a naming clash to clear up first, since "users" means two
very different things.

## Step 1 — Two different kinds of "users"

- An **application-level user** — like a row in a `customers` table — is
  just data. Anyone with the right permissions can read or write it.
- A **database-level user (role)** — what this lesson covers — is
  PostgreSQL's own login identity: *who* is allowed to connect to the
  database at all, and *what* they're allowed to do once connected.

So far, every example in this course has run as the all-powerful `postgres`
superuser. Real applications never should — this lesson fixes that.

## Step 2 — `CREATE ROLE` and `CREATE USER`

```sql
CREATE ROLE app_user WITH LOGIN PASSWORD 'change_me_123';
```

`CREATE USER` is identical, just shorthand — a "user" is simply a role
created with `LOGIN` permission built in:

```sql
CREATE USER app_user WITH PASSWORD 'change_me_123';   -- LOGIN is implied
```

Right now, `app_user` can connect — but can't touch a single table. Every
permission has to be granted explicitly.

## Step 3 — `GRANT`: giving specific permissions

```sql
GRANT SELECT, INSERT, UPDATE ON products, orders, order_items TO app_user;
```

`app_user` can now read, insert, and update rows in exactly those 3 tables —
notice **not** `DELETE`, and **not** `customers`, `reviews`, or any other
table. This is the **principle of least privilege**: grant exactly what's
needed, nothing more — the same instinct behind
[Lesson 2.13](13-constraints.md)'s constraints, just applied to *who* can act,
not *what values* are allowed.

## Step 4 — `REVOKE`: taking a permission back

```sql
REVOKE UPDATE ON products FROM app_user;
```

`app_user` can still `SELECT` and `INSERT` on `products`, but no longer
`UPDATE` it — maybe price changes should only happen through a separate,
more tightly controlled process.

## Step 5 — Role membership: groups of permissions

Rather than repeating the same `GRANT`s for every new role, define a
reusable "template" role, and let others inherit from it:

```sql
CREATE ROLE read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;

CREATE ROLE analyst WITH LOGIN PASSWORD 'analyst_pw_123';
GRANT read_only TO analyst;   -- analyst now inherits every SELECT read_only has
```

`analyst` can now query every table — but never `INSERT`, `UPDATE`, or
`DELETE` anything, anywhere. Add a new table later, re-run one `GRANT` on
`read_only`, and every role that inherits from it picks up the change
automatically.

## Step 6 — `ALTER ROLE` and `DROP ROLE`

```sql
ALTER ROLE app_user WITH PASSWORD 'a_much_better_password_456';
```

```sql
DROP ROLE analyst;
-- ERROR, if analyst still owns objects or has pending grants —
-- reassign or revoke those first, then DROP ROLE again
```

## Step 7 — A realistic role setup for our schema

Pulling this together for the actual `apple_store` database from
[Lesson 2.2](02-your-first-database-apple-example.md):

```sql
-- The application itself: read/write its own operational tables only
CREATE ROLE app_user WITH LOGIN PASSWORD 'change_me_123';
GRANT SELECT, INSERT, UPDATE ON products, customers, orders, order_items TO app_user;

-- Read-only reporting/BI access
CREATE ROLE read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;

CREATE ROLE analyst WITH LOGIN PASSWORD 'analyst_pw_123';
GRANT read_only TO analyst;
```

Notice neither role can `DROP TABLE`, `DELETE` arbitrary data, or manage
other roles — capabilities reserved for whoever administers the database
directly (still `postgres`, used sparingly, by a human, not an application).

## Step 8 — Recap

| Command | Does |
|---|---|
| `CREATE ROLE` / `CREATE USER` | Creates a new database login identity |
| `GRANT ... ON ... TO ...` | Gives a specific permission on specific tables |
| `REVOKE ... ON ... FROM ...` | Takes a permission back |
| `GRANT role TO role` | One role inherits another's permissions (group membership) |
| `ALTER ROLE ... WITH PASSWORD ...` | Changes a role's password |
| `DROP ROLE` | Deletes a role (after clearing anything it owns) |

---
← [2.17 Create Tables: More Examples](17-create-tables-examples.md) | Next: [2.19 Capstone →](19-capstone.md)
