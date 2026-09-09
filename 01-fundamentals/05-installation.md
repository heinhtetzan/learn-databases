← [1.4 Database Brands](04-database-brands.md)

# 1.5 Installing PostgreSQL & MongoDB

[Lesson 1.4](04-database-brands.md) split this course into two hands-on
parts — PostgreSQL for SQL, MongoDB for NoSQL. Before either one, let's get
both actually installed and running.

## Step 1 — What you need, and when

You only need **PostgreSQL** right now to start Part 1
([02-sql/](../02-sql/)). Install **MongoDB** whenever you're ready for
Part 2 — feel free to skip that section today and come back to it later.

| | Needed for | Default port |
|---|---|---|
| PostgreSQL | Part 1 — SQL | 5432 |
| MongoDB | Part 2 — NoSQL | 27017 |

## Step 2 — Installing PostgreSQL

### macOS

**Option A — Postgres.app (easiest, no terminal required):**
1. Download it from [postgresapp.com](https://postgresapp.com).
2. Drag it into `Applications`, open it, click **Initialize**.
3. It runs in your menu bar and starts automatically — nothing else to configure.

**Option B — Homebrew:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

### Windows

1. Download the installer from
   [postgresql.org/download/windows](https://www.postgresql.org/download/windows/).
2. Run it — accept the defaults, and **remember the password** you set for
   the `postgres` user; you'll need it to connect.
3. Leave "Stack Builder" unchecked at the end unless you specifically need it.

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql   # auto-start on every boot
```

### Verify it's running

```bash
psql --version
psql -U postgres
```

If `psql -U postgres` connects and shows a `postgres=#` prompt, you're set.
Now create the database this whole course uses:

```sql
CREATE DATABASE apple_store;
\c apple_store
```

This is exactly [Lesson 2.2](../02-sql/02-your-first-database-apple-example.md)'s
Step 1 — you're now ready to start Part 1 for real.

## Step 3 — Installing MongoDB

### macOS (Homebrew)

```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

### Windows

1. Download the MSI installer from
   [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community).
2. Run it, choosing **"Install MongoDB as a Service"** when prompted — it
   then starts automatically in the background.

### Linux (Ubuntu)

```bash
# Import MongoDB's package signing key and repo (see mongodb.com docs for
# the exact commands for your Ubuntu version — they change slightly per release)
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Verify it's running

```bash
mongosh --version
mongosh
```

If `mongosh` connects and shows a `test>` prompt, MongoDB is ready — you'll
use this when Part 2 begins.

## Step 4 — GUI tools (optional, but genuinely helpful)

Typing every command in a terminal isn't required — these visual tools make
browsing data much easier, especially early on:

| Tool | Works with | Notes |
|---|---|---|
| **pgAdmin** | PostgreSQL only | The standard, official PostgreSQL GUI |
| **MongoDB Compass** | MongoDB only | The standard, official MongoDB GUI |
| **TablePlus** / **DBeaver** | Both, plus most other databases | One tool for everything — a nice option once you're using both parts of this course |

## Step 5 — No local install? Use a free cloud database instead

Every example in this course also works against a free-tier cloud database —
useful if you can't install software locally (a locked-down work laptop, a
Chromebook, etc.):

- **PostgreSQL**: [Neon](https://neon.tech) or [Supabase](https://supabase.com)
  — both have a free tier; sign up, create a project, and you'll get a
  connection string to paste into any PostgreSQL client. For quick one-off
  testing without even signing up, [DB Fiddle](https://www.db-fiddle.com/)
  runs PostgreSQL right in the browser.
- **MongoDB**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) — create
  a free **M0** cluster, and Atlas gives you a connection string for
  `mongosh` or Compass.

## Step 6 — Recap checklist

- [ ] PostgreSQL installed (or a cloud project created)
- [ ] `psql -U postgres` connects successfully
- [ ] `apple_store` database created
- [ ] *(Whenever you reach Part 2)* MongoDB installed (or an Atlas cluster created)
- [ ] *(Whenever you reach Part 2)* `mongosh` connects successfully

With PostgreSQL running, you're ready to either start
[Part 1 — SQL](../02-sql/01-what-is-sql.md) directly, or read
[Lesson 1.6](06-run-with-docker.md) first for a Docker-based alternative to
everything above.

---
← [1.4 Database Brands](04-database-brands.md) | Next: [1.6 Running with Docker →](06-run-with-docker.md)
