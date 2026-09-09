← [3.17 Create Collections: More Examples](17-create-collections-examples.md)

# 3.18 User & Access Management

Same distinction as [Lesson 2.18](../02-sql/18-user-access-management.md) —
an application-level "user" (a document in a `customers` collection) is just
data; a **database user** is MongoDB's own login identity, with its own
permissions.

## Step 1 — `db.createUser()`

```js
db.createUser({
  user: "app_user",
  pwd: "change_me_123",
  roles: [{ role: "readWrite", db: "apple_store" }]
});
```

`app_user` can now read and write anything in `apple_store` — MongoDB's
built-in roles are broader by default than SQL's per-table `GRANT`
([Lesson 2.18](../02-sql/18-user-access-management.md)); scoping permissions
to *specific collections* needs a custom role instead.

## Step 2 — Built-in roles

| Role | Grants |
|---|---|
| `read` | Read-only, on one database |
| `readWrite` | Read + write, on one database |
| `dbAdmin` | Manage indexes, schema validation — not data itself |
| `userAdmin` | Manage other users' roles |
| `readWriteAnyDatabase` | `readWrite`, across every database on the server |

## Step 3 — A custom role: least privilege, precisely

```js
db.createRole({
  role: "orderProcessor",
  privileges: [
    { resource: { db: "apple_store", collection: "orders" },       actions: ["find", "insert", "update"] },
    { resource: { db: "apple_store", collection: "order_items" },  actions: ["find", "insert", "update"] },
    { resource: { db: "apple_store", collection: "products" },     actions: ["find", "update"] }
  ],
  roles: []
});

db.createUser({
  user: "app_user",
  pwd: "change_me_123",
  roles: ["orderProcessor"]
});
```

Same principle as [Lesson 2.18](../02-sql/18-user-access-management.md)'s
`GRANT SELECT, INSERT, UPDATE ON products, orders, order_items TO app_user`
— explicit actions, on explicit collections, nothing more.

## Step 4 — Role inheritance

```js
db.createRole({
  role: "readOnly",
  privileges: [
    { resource: { db: "apple_store", collection: "" }, actions: ["find"] }   // "" = every collection
  ],
  roles: []
});

db.createUser({
  user: "analyst",
  pwd: "analyst_pw_123",
  roles: ["readOnly"]
});
```

Direct equivalent of [Lesson 2.18](../02-sql/18-user-access-management.md)'s
`read_only` role pattern — `analyst` can query every collection, and never
insert, update, or delete anything.

## Step 5 — Changing permissions and passwords

```js
db.grantRolesToUser("app_user", ["readOnly"]);      // add a role
db.revokeRolesFromUser("app_user", ["readOnly"]);    // remove one

db.updateUser("app_user", { pwd: "a_much_better_password_456" });

db.dropUser("analyst");
```

## Recap

| SQL ([Lesson 2.18](../02-sql/18-user-access-management.md)) | MongoDB |
|---|---|
| `CREATE ROLE`/`CREATE USER` | `db.createUser()` |
| `GRANT ... ON ... TO ...` | A custom role's `privileges`, assigned via `roles: [...]` |
| `REVOKE` | `db.revokeRolesFromUser()` |
| Role membership | `roles: [...]` on `createRole`/`createUser` |
| `ALTER ROLE ... WITH PASSWORD` | `db.updateUser()` |
| `DROP ROLE` | `db.dropUser()` |

---
← [3.17 Create Collections: More Examples](17-create-collections-examples.md) | Next: [3.19 Capstone →](19-capstone.md)
