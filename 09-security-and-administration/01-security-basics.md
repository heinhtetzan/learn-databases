← [Module 09](README.md) | [Course Home](../README.md)

# 9.1 Database Security Basics

## Principle of least privilege

Every user or application should have the **minimum** access it needs to do its
job — nothing more. This single principle prevents most database security
incidents from becoming catastrophic.

```sql
-- Create a role for your application with only the access it needs
CREATE ROLE app_user LOGIN PASSWORD 'use-a-secrets-manager-not-this';
GRANT SELECT, INSERT, UPDATE ON orders, order_items TO app_user;
GRANT SELECT ON books, authors TO app_user;
-- Notice: no DELETE, no DROP, no access to a 'customers.payment_info' column, etc.

-- A separate, more limited role for a read-only analytics dashboard
CREATE ROLE analytics_readonly LOGIN PASSWORD '...';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_readonly;

-- A separate, powerful role only for migrations — used rarely, not by the app itself
CREATE ROLE migrations_admin LOGIN PASSWORD '...';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO migrations_admin;
```

**Never** have your everyday application connect using a database
superuser/root account — if that connection is ever compromised (a leaked
credential, an injection vulnerability below), the blast radius is the entire
database instead of a limited set of tables/operations.

## Column and row-level security

Beyond table-level grants, most production databases support finer control:

```sql
-- Row-level security (PostgreSQL): each customer can only see their own orders
CREATE POLICY customer_own_orders ON orders
    USING (customer_id = current_setting('app.current_customer_id')::int);
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
```

Useful for multi-tenant applications where you want the database itself — not
just application code — to guarantee tenant isolation.

## SQL Injection

The single most important application-security topic connected to databases.
It happens when untrusted input is concatenated directly into a SQL string:

```python
# ❌ VULNERABLE — never do this
query = f"SELECT * FROM customers WHERE email = '{user_input}'"
# If user_input is:  ' OR '1'='1
# The query becomes: SELECT * FROM customers WHERE email = '' OR '1'='1'
# ...which matches EVERY row, leaking every customer's data
```

A more damaging classic example:

```python
# ❌ VULNERABLE
query = f"SELECT * FROM customers WHERE email = '{user_input}'"
# If user_input is:  '; DROP TABLE customers; --
# The query becomes two statements (in databases/drivers that allow this):
#   SELECT * FROM customers WHERE email = '';
#   DROP TABLE customers; --'
```

### The fix: parameterized queries (prepared statements)

```python
# ✅ SAFE — the driver sends the query and the value SEPARATELY;
# the value is never interpreted as SQL syntax, no matter what it contains
cursor.execute("SELECT * FROM customers WHERE email = %s", (user_input,))
```

```sql
-- ✅ SAFE — parameterized in raw SQL (driver-dependent placeholder syntax)
PREPARE get_customer (text) AS SELECT * FROM customers WHERE email = $1;
EXECUTE get_customer('alice@mail.com');
```

**Rule with no exceptions**: never build a SQL string by concatenating or
interpolating raw user input, ever — always use parameterized
queries/prepared statements, or a well-tested query builder/ORM that does this
for you under the hood. This single practice eliminates SQL injection
entirely, regardless of what the input contains.

## Encryption

| Type | Protects against | How |
|---|---|---|
| **Encryption in transit** | Network eavesdropping between app and database | TLS/SSL connections (`sslmode=require` in Postgres connection strings) |
| **Encryption at rest** | Someone stealing the physical disk/backup files | Full-disk or filesystem-level encryption; most managed cloud databases enable this by default |
| **Column-level encryption** | Even database admins/backups seeing specific sensitive fields in plaintext | Application-level encryption of specific columns (e.g., SSNs) before they're ever sent to the database |

## Auditing

Log who accessed or changed what, and when — critical for detecting breaches
after the fact and for regulatory compliance (HIPAA, PCI-DSS, GDPR, etc.). Most
production databases support audit logging as a built-in or extension feature
(e.g., PostgreSQL's `pgaudit`).

## A practical security checklist

- [ ] Application connects with a limited-privilege role, never a superuser
- [ ] All connections use TLS
- [ ] All queries are parameterized — no string concatenation of user input, anywhere
- [ ] Secrets (passwords, connection strings) live in a secrets manager, never in
      source code or plain-text config files
- [ ] Sensitive columns (payment info, SSNs) are encrypted or tokenized
- [ ] Backups are encrypted too — a stolen backup is just as bad as a stolen live database
- [ ] Access is logged/audited, especially for admin-level roles

## Try it yourself

1. Design roles (with specific `GRANT`s) for the bookstore application: one for
   the customer-facing web app, one for an internal admin dashboard that can
   manage inventory, and one read-only role for a reporting tool.
2. Take this vulnerable snippet and rewrite it safely:
   `query = "SELECT * FROM books WHERE title = '" + search_term + "'"`.
3. Explain, in your own words, why encrypting a database's backups matters just
   as much as encrypting the live database itself.

---
← [Module 09](README.md) | Next: [Backup & Recovery →](02-backup-recovery.md)
