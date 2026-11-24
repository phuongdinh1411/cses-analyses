---
layout: simple
title: "Database Transactions — System Design School"
permalink: /system_design/sds/concepts/domain-transactions
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

Lessons

Your progress0%

AllSaved

Concurrency & Transactions

Concurrency

- Concurrency Fundamentals

- Race Conditions

- Mutexes and Read-Write Locks

- Semaphores

- Deadlocks

- Distributed Locks

Transactions

- Database Transactions

- Database Isolation Levels

- Database Locking & Concurrency

- Pessimistic Locking Strategies

- Optimistic Locking Patterns

- Atomic CAS & Holds

- Flash Sale Inventory Patterns

Distributed Systems

Search, Feeds & Spatial

Specialized Systems & Data Structures

# Database Transactions

Start quizSave

A multi-step write across multiple rows can leave a database half-updated when a process crashes or a statement fails mid-flight. A database transaction groups a sequence of reads and writes into a single logical unit so that all changes commit together or none of them take effect.

## Why Single Statements Are Not Enough

Consider a bank transfer of 100 USD from account A (balance 500) to account B (balance 200), where total funds across both accounts must stay 700. Without a transaction, the database executes and commits each UPDATE independently. If the application server crashes after debiting account A, account A holds 400 while account B still holds 200, and 100 USD disappears.

A second failure happens under concurrency when two buyers read available = 1 for seat 12A at the same time. Both proceed to decrement the count and insert a ticket row, selling the same seat twice. Wrapping related reads and writes inside an explicit transaction gives the database engine a boundary to enforce atomicity and isolate concurrent writers.

Press "Next step" to watch an unprotected transfer lose 100 USD after a crash, then switch Mode to "One transaction" to see crash recovery restore the original balances.

Scenario

Transfer 100 USDTwo buyers, one seat

Mode

Each statement on its ownOne transaction

Crash after the debit

Next stepPlayResetStep 0 of 3

accounts table

id

balance

A

500

B

200

Total

700

Statements

AppUPDATE accounts SET balance = balance - 100 WHERE id = 'A'

Server-- crash before the credit runs

Database-- restart and recovery

Transfer 100 USD from A (500) to B (200). The total is 700. The server will crash after the debit. Press "Next step".

The locking and re-check follow PostgreSQL at its default Read Committed level. Balances and seat counts are the lesson's example.

## Transaction Lifecycle and Boundaries

A client opens a transaction with BEGIN, runs one or more SQL statements, and closes it with COMMIT or ROLLBACK. The database engine assigns each active transaction a unique identifier (txid) so it can track locks, log entries, and row versions belonging to that unit of work.

BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
INSERT INTO transfers (from_account, to_account, amount) VALUES ('A', 'B', 100);
COMMIT;

Every transaction moves through a fixed set of states and terminates in either Committed or Aborted.

A transaction starts in the Active state while executing statements. When the client issues COMMIT, the transaction enters Partially Committed until its commit record reaches non-volatile storage. Once the flush succeeds, the transaction becomes Committed and releases its locks. If any statement violates a constraint, the client issues ROLLBACK, or the server crashes before the commit record is flushed, the transaction transitions to Failed and then Aborted after its changes are undone.

## ACID Properties Under the Hood

Relational databases express their transactional contract through four properties known as ACID: Atomicity, Consistency, Isolation, and Durability. Each property maps to concrete mechanisms inside the storage engine.

### Atomicity: All or Nothing via Undo Logs and WAL

Atomicity ensures that a transaction either applies every one of its writes or leaves the database unchanged. A partial write is never exposed to other transactions after a failure or crash.

Storage engines implement atomicity with an undo log or with multi-version row storage. Before overwriting a record in place, an undo-based engine writes the previous value (the before-image) to an undo log. If the transaction rolls back or the server crashes before a commit record is written to the Write-Ahead Log (WAL), the engine replays the undo records in reverse order to restore the original rows. In multi-version engines such as PostgreSQL, uncommitted row versions carry the writing transaction's txid and are ignored by other readers if that txid never commits.

### Consistency: Preserving Invariants

Consistency means every committed transaction moves the database from one valid state to another while preserving all defined invariants. An invariant is a rule that must hold before and after every transaction, such as balance >= 0, available_seats >= 0, unique email addresses, or valid foreign keys.

Consistency is a shared responsibility between the database and the application. The database enforces declared schema rules (CHECK, UNIQUE, NOT NULL, FOREIGN KEY) and aborts any transaction that breaks them. Application code is still responsible for writing correct business logic inside the transaction, because the database cannot know that debiting account A without crediting account B violates an accounting invariant unless both statements are included.

### Isolation: Preventing Concurrent Interference

Isolation controls how concurrent transactions observe each other's in-flight changes. Ideal serializable isolation makes concurrent transactions produce the same final state as if they had executed one after another.

Without row locking or a stronger isolation level, two concurrent transactions can both read available = 1 for seat 12A and both write available = 0. A guarded write (UPDATE seats SET available = available - 1 WHERE seat_id = '12A' AND available >= 1) or an explicit row lock (SELECT ... FOR UPDATE) forces the second buyer to wait until the first commits, then re-evaluate the condition against the updated row. The full range of isolation guarantees and anomalies is covered in Database Isolation Levels, and lock mechanics are covered in Database Locking & Concurrency.

### Durability: Surviving Crashes with WAL and fsync

Durability guarantees that once the database acknowledges COMMIT, the transaction's changes survive process crashes and power loss. Updating scattered B-tree data pages directly on disk for every commit would require random disk writes and slow down commit throughput.

Instead, databases append every change sequentially to the Write-Ahead Log (WAL) before modifying data pages on disk. On COMMIT, the engine writes a commit record to the WAL buffer and calls fsync() to flush that sequential buffer from the OS page cache to non-volatile storage before returning success to the client.

Dirty pages in the buffer pool (the database's in-memory page cache) are flushed to the main data files later in the background during a checkpoint. A checkpoint records a point in the WAL up to which all modified pages are safely on disk, which bounds how much log the engine must scan after a crash. On restart, crash recovery reads the WAL forward from the last checkpoint to redo committed transactions whose pages never reached the data files, and undoes any uncommitted transactions that lack a commit record.

Durability beyond one disk. Local fsync() protects against process crashes and power loss, while surviving a destroyed disk or failed host requires replicating the WAL to standby nodes in another failure domain.

## Defining Transaction Boundaries in Practice

Keeping transactions short is the main operational rule for high-concurrency databases. An open transaction holds row locks on every record it modifies and prevents multi-version storage engines from reclaiming old row versions, so long-lived transactions cause lock queues and table bloat.

A common mistake is placing external network calls—such as charging a third-party payment gateway or sending a confirmation email—inside an open database transaction. If the external API stalls, the database connection and its row locks remain pinned for the entire wait.

-- Keep the database transaction limited to state transitions
BEGIN;
UPDATE inventory SET stock = stock - 1 WHERE item_id = 'laptop' AND stock >= 1;
-- Application checks affected_rows == 1; if 0, ROLLBACK and return out-of-stock
INSERT INTO orders (user_id, item_id, status) VALUES ('alice', 'laptop', 'pending_payment');
INSERT INTO outbox_events (event_type, payload) VALUES ('order_created', '{"order_id": 42}');
COMMIT;
-- Background workers process payment API calls and confirmation emails asynchronously

OperationPlacementReason

Balance transfer, stock decrement, order creationInside transactionMultiple rows must commit or roll back together to preserve invariants

Outbox event insert for downstream workflowsInside transactionGuarantees an event exists if and only if the state change commits

Payment gateway HTTP call, email, push notificationOutside transactionExternal I/O can stall and hold database locks open

Large batch backfill or analytics scanOutside single transactionLong-running snapshots pin undo logs and block vacuuming

When a transaction must lock multiple rows—such as transferring money between two accounts—acquiring those locks in a consistent canonical order (for example, sorted by primary key id) prevents circular wait deadlocks. Applications should still catch deadlock or serialization errors, roll back cleanly, and retry with bounded exponential backoff and jitter.

Key idea. A database transaction groups multiple statements into one atomic unit backed by undo logs (or multi-version storage) for rollback and a sequentially flushed Write-Ahead Log (fsync) for crash durability. Keep transaction boundaries strictly around database state changes, move external network calls outside the transaction via async queues or an outbox table, and acquire multi-row locks in a consistent order to avoid deadlocks.

The next lesson, Database Isolation Levels, examines what happens when multiple transactions run concurrently and which anomalies each SQL isolation level prevents.

Explain

Add to Chat

Start QuizLoading

Send feedback
