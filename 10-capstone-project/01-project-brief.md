← [Module 10](README.md) | [Course Home](../README.md)

# 10.1 Project Brief: RideShare — A Ride-Booking Platform

## The brief

> Design the database for **RideShare**, a ride-booking platform. Requirements,
> as given by the (fictional) product team:
>
> - Riders create accounts and request rides between a pickup and drop-off
>   location.
> - Drivers create accounts, own a vehicle (make, model, license plate), and
>   accept ride requests.
> - A ride goes through states over time: `requested` → `accepted` →
>   `in_progress` → `completed` (or `cancelled` at almost any point before
>   completion).
> - Once completed, a ride has a fare, computed from distance and duration, and
>   both the rider and driver can leave a rating (1–5) and optional comment
>   about each other.
> - Drivers' live GPS locations update every few seconds while online, and the
>   app needs to find "available drivers near this rider" quickly.
> - Payments are processed by a separate third-party payment provider — the
>   platform just needs to record the payment amount, status, and provider's
>   transaction reference for each completed ride.
> - The company is starting with one city, but plans to expand to hundreds of
>   cities within two years, and needs the system to handle that growth without
>   a redesign.

## Your tasks

Work through these in order — each maps directly to a module you've completed.
Write your answers down (a scratch `.md` file, or directly in a copy of this
file) before checking the solution guide.

### 1. ER Modeling ([Module 04](../04-schema-design/01-er-modeling.md))
Identify every entity, its key attributes, and every relationship with correct
cardinality. Pay close attention to the rider ↔ driver rating requirement — it's
subtler than it first looks.

### 2. Schema & DDL ([Modules 02–04](../02-relational-model/))
Write full `CREATE TABLE` statements: primary keys, foreign keys with sensible
`ON DELETE` behavior, `CHECK` constraints for the ride state machine and rating
range, and a normalized structure (aim for 3NF, and justify any deliberate
denormalization).

### 3. Core Queries ([Module 03](../03-sql-fundamentals/))
Write SQL for:
- A rider's full ride history with driver name, fare, and their given rating.
- Each driver's average rating and total completed rides.
- The single busiest hour of the day, by completed ride count.

### 4. Indexing ([Module 05](../05-indexing-performance/))
Identify at least 4 indexes this schema needs, and justify each by naming the
specific query pattern it supports.

### 5. Transactions & Concurrency ([Module 06](../06-transactions-concurrency/))
Two riders in the same area both request a ride at nearly the same instant,
and the system tries to match both to the same single available driver. Design
the transaction/locking approach that guarantees only one match succeeds.

### 6. NoSQL Considerations ([Module 07](../07-nosql/))
The live GPS location requirement ("find available drivers near this rider,
updated every few seconds") doesn't fit the relational model well. Propose
which NoSQL category (if any) you'd bring in specifically for this piece, and
justify it — this is a polyglot-persistence decision.

### 7. Scaling ([Module 08](../08-scaling-and-replication/))
The platform needs to support "hundreds of cities" within two years. Propose a
sharding strategy (and shard key) for the ride/rider/driver data, and identify
one query from Task 3 that would become a cross-shard query under your
strategy.

### 8. Security & Backup ([Module 09](../09-security-and-administration/))
Propose database roles for: the rider/driver-facing app, an internal support
dashboard (which needs to view but not delete ride history), and a data
analytics pipeline. Propose an RPO/RTO for ride and payment-reference data, and
justify it.

## What "done" looks like

A complete solution is: an ER diagram, full DDL, the requested queries, a list
of justified indexes, a written explanation of your concurrency-safe matching
approach, a NoSQL/polyglot recommendation with justification, a sharding
proposal, and a security/backup plan — each with a one- or two-sentence
justification, not just an answer.

---
← [Module 10](README.md) | Next: [Solution Guide →](02-solution-guide.md)
