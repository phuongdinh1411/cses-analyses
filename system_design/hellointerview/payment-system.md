---
layout: simple
title: "Design a Payment System (Stripe) — Hello Interview Style"
permalink: /system_design/hellointerview/payment-system
---

# Payment System (Stripe)

**Patterns:** Multi-step Processes  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Charging exactly once at 10K TPS despite slow, unreliable card-network calls (2–5s), while staying PCI-compliant and never losing transaction data.
- **Core design:** Merchants create PaymentIntents; Stripe.js sends card data directly to an HSM-backed vault; the Payment Processor scores fraud, authorizes via the card network through an outbox poller, updates PostgreSQL, and publishes events to Kafka for webhooks, audit, and analytics.
- **Techniques:** tokenization + HSM vault (no raw card storage); idempotency keys (no double charges); transactional outbox (safe external calls); authorize-then-capture (hold before charge); append-only audit log / event sourcing (auditability); synchronous replication (zero loss); shard by merchant_id.

## Understanding the Problem

💳 **What is Stripe?**  
Stripe allows merchants to accept payments from customers without building their own payment infrastructure. Customers enter payment details on the merchant site, the merchant sends them to Stripe, and Stripe processes the payment and returns the result.

**Payment flow actors:**
- **Merchant** – e-commerce site collecting payment
- **Customer** – the person paying
- **Stripe (us)** – payment processor
- **Card Networks** – Visa, Mastercard (route payments)
- **Issuing Bank** – customer's bank (authorizes/declines)
- **Acquiring Bank** – merchant's bank (receives funds)

---

### Functional Requirements

**Core Requirements**

- Merchants should be able to initiate payment requests (charge a customer for a specific amount)
- Users should be able to pay for products with credit/debit cards
- Merchants should be able to view status updates for payments (pending, success, failed)

**Below the line (out of scope):**

- Saving payment methods for future use
- Issuing refunds
- Transaction history and reports
- Alternative payment methods (bank transfers, wallets)
- Recurring payments / subscriptions
- Payouts to merchants

### Non-Functional Requirements

**Core Requirements**

- The system must be **highly secure** (PCI-DSS compliant, no raw card data stored)
- The system must guarantee **durability and auditability** — no transaction data ever lost
- The system must handle payment **exactly once** (no double charges)
- The system must be **highly available** (payments must work 24/7)
- The system should scale to **10,000 TPS** at peak

**Below the line (out of scope):**

- Sub-millisecond payment processing (< 3 seconds acceptable for card payments)

### Constraints & Estimates

- 10K TPS peak
- Each payment has ~5 state transitions → 50K status updates/sec
- Payment record: ~2KB
- 10K × 2KB = 20MB/sec write throughput
- Average payment processing: 2–5 seconds (network calls to card networks)

---

## The Set Up

### Defining the Core Entities

- **PaymentIntent** – id, merchant_id, amount, currency, status (created/processing/succeeded/failed), customer_id, metadata, idempotency_key, created_at, updated_at
- **PaymentMethod** – id, type (card), last4, brand (Visa/MC), exp_month, exp_year, card_fingerprint (tokenized)
- **Charge** – id, payment_intent_id, amount, currency, status, failure_reason, card_network_ref, created_at
- **AuditLog** – id, entity_type, entity_id, action, previous_state, new_state, timestamp, actor_id

### API or System Interface

```
// Merchant creates a payment intent (server-side)
POST /payment_intents
{ "amount": 5000, "currency": "usd", "customer_id": "cus_123", "metadata": { "order_id": "ord_456" } }
-> { payment_intent_id: "pi_abc", client_secret: "pi_abc_secret_xyz", status: "created" }

// Customer submits card details (client-side, using Stripe.js — card data never touches merchant server)
// Stripe.js calls Stripe directly with the client_secret
POST /payment_intents/{id}/confirm
{ "payment_method": { "card": { "number": "4242...", "exp_month": 12, "exp_year": 2025, "cvc": "123" } } }
-> { status: "processing" | "succeeded" | "failed" }

// Get payment status (merchant polls or uses webhook)
GET /payment_intents/{id}
-> { payment_intent_id, status, amount, currency, created_at }

// Webhook: Stripe notifies merchant of status changes
POST {merchant_webhook_url}
{ "event": "payment_intent.succeeded", "data": { payment_intent_id, amount, ... } }
```

---

## High-Level Design

### 1) Merchants should be able to initiate payment requests

**Server-side (merchant backend → Stripe API):**

1. Merchant calls `POST /payment_intents` with amount + currency
2. Stripe creates a PaymentIntent record (status=created)
3. Returns `client_secret` — a temporary token that authorizes the customer to complete payment on the client side

**Why payment intents?** Separates the merchant's decision to charge from the customer's act of paying. Allows Stripe to handle payment method collection securely on the client side without the merchant ever seeing raw card data.

**PaymentIntent lifecycle:**
```
created → processing → succeeded
                    → failed
                    → requires_action (3D Secure challenge)
```

### 2) Users should be able to pay with credit/debit cards

**Client-side card collection (Stripe.js / Elements):**
- Customer enters card details in a Stripe-hosted iframe embedded in the merchant page
- Card details are submitted **directly to Stripe's servers** — never touch the merchant's backend
- Stripe tokenizes the card → stores only a fingerprint + last4 in its DB
- PCI-DSS scope is drastically reduced (merchant is never in scope for raw card data)

**Payment processing flow:**

```
Customer submits card via Stripe.js
  → Stripe Confirm API: POST /payment_intents/{id}/confirm
  → Payment Processor Service:
    1. Tokenize card → store PaymentMethod (last4, exp, fingerprint, vault token)
    2. Run fraud checks (velocity checks, card fingerprint, geolocation)
    3. Call Card Network (Visa/MC) for authorization:
       POST https://api.visa.com/authorize { amount, merchant_id, card_token }
    4. Card Network contacts Issuing Bank → approve/decline
    5. Receive authorization code
    6. Update PaymentIntent status = succeeded / failed
    7. Write Charge record
    8. Send webhook to merchant
```

### 3) The system should provide status updates for payments

**Two mechanisms:**

**A) Synchronous response:** The `/confirm` call waits (< 5s) for the authorization response and returns final status directly.

**B) Webhooks (async):** For asynchronous state changes (e.g., 3D Secure pending, chargeback later):
- Stripe calls merchant's webhook URL with signed payload
- Webhook signing: HMAC-SHA256 with merchant's secret key → merchant verifies signature

---

## Potential Deep Dives

### 1) The system should be highly secure

**PCI-DSS compliance:**
- **Never store raw card numbers or CVVs** — tokenize immediately using a Hardware Security Module (HSM)
- Card vault: raw card data encrypted with HSM-managed keys, stored in isolated vault service with no network egress except to card networks
- Separate network zone for cardholder data environment (CDE)
- TLS 1.3 everywhere
- mTLS between internal services in the payment path

**Tokenization flow:**
```
Customer card → Stripe.js → Stripe ingest API (HSM vault)
  → Store encrypted card in vault, return vault_token
  → Subsequent operations use vault_token only (never raw card)
  → Card network call: HSM decrypts card momentarily to send to Visa/MC
```

**Fraud detection:**
- Real-time scoring before authorization: card velocity (too many charges in 1 hour), IP geolocation mismatch, device fingerprint, ML model
- Threshold: block payments with fraud score > 0.9; flag for review at > 0.7

### 2) The system should guarantee durability and auditability

**Immutable audit log:**
- Every state transition of every PaymentIntent is appended to an immutable `audit_log` table
- Write-once, never update (append-only)
- Stored in a separate DB with no UPDATE/DELETE permissions
- Also streamed to S3 for cold storage and compliance

**Write-ahead logging (WAL):**
- PostgreSQL WAL ensures no committed transaction is lost even on crash
- Synchronous replication to standby: `synchronous_commit = on` — write not acknowledged until standby confirms

**Event sourcing:**
- PaymentIntent state is rebuilt from an immutable sequence of events:
  ```
  PaymentIntentCreated
  PaymentMethodAttached
  AuthorizationRequested
  AuthorizationApproved
  ChargeCreated
  ```
- Current state = replay of events (no update queries, only appends)
- Full audit trail for regulatory compliance

### 3) The system should guarantee transaction safety despite async payment networks

**Problem:** We call the card network (async, unreliable). What if:
- We send authorization request but never get a response (network timeout)?
- We get a success response but crash before writing to our DB?

**Outbox pattern + idempotent retries:**

```
Transaction:
  BEGIN;
  INSERT INTO payment_intents (id, status=processing, ...);
  INSERT INTO outbox_events (type=authorization_request, payload={...});
  COMMIT;

Outbox Poller (async):
  - Poll outbox_events for unprocessed events
  - Call card network with idempotency_key = payment_intent_id
  - On success: UPDATE payment_intents SET status=succeeded; DELETE FROM outbox
  - On timeout: retry (card network deduplicates via idempotency_key)
```

**Idempotency at card network:**
- Include `idempotency_key` in authorization request (usually the PaymentIntent ID)
- If network timeouts and we retry: card network returns the same authorization response (not a double charge)

**Two-phase approach:**
1. **Authorization** – card network holds funds (no charge yet)
2. **Capture** – after merchant confirms order shipped, actually charge the card

If authorization succeeds but capture fails: funds are automatically released after 7 days (no charge).

### 4) The system should be scalable to handle 10,000+ TPS

#### Servers

- **Stateless API servers**: auto-scale behind load balancer; 10K TPS at 50ms avg → 500 concurrent requests → ~10 servers (~50 concurrent ≈ 1K req/sec each) + headroom
- Each payment path: DB write + external card network call (2–5s) → real bottleneck is external call latency, not our compute

#### Kafka

- Each payment state transition published to Kafka:
  - Webhook delivery: Kafka → Webhook Worker → merchant webhook URL
  - Analytics: Kafka → ClickHouse (real-time fraud dashboards)
  - Audit: Kafka → S3 (durable audit trail)
- 10K TPS × 5 events/payment = 50K events/sec → easily handled by Kafka (millions/sec capacity)

#### Database

- **Primary-replica PostgreSQL cluster** (1 primary, 3 replicas)
- **Shard by merchant_id**: each merchant's payments go to the same shard → queries are always merchant-scoped
- **Write path**: PaymentIntent create/update → primary
- **Read path**: merchant dashboard queries → read replica
- **Connection pooling**: PgBouncer pools 10K TPS into manageable DB connections (PostgreSQL max ~1K connections)

---

## Final Design

```
Customer Browser
  │ Stripe.js (card details directly to Stripe)
  ▼
API Gateway (TLS termination, rate limiting)
  │
  ├─ [Create PaymentIntent] → Payment Intent Service → PostgreSQL (write primary)
  │                         → Outbox: authorization_request event
  │
  ├─ [Confirm] → Payment Processor Service
  │              ├─ Card Vault (HSM) → tokenize card
  │              ├─ Fraud Engine → score
  │              ├─ Outbox Poller → Card Network (Visa/MC) API → Issuing Bank
  │              ├─ Update PaymentIntent (succeeded/failed) → PostgreSQL
  │              └─ Publish to Kafka → Webhook Worker → Merchant webhook
  │
  └─ [Get Status] → Payment Intent Service → PostgreSQL read replica

PostgreSQL (sharded by merchant_id)
  - payment_intents, charges, payment_methods, audit_log (append-only)

Kafka
  → Webhook Worker (at-least-once delivery to merchants)
  → S3 (audit log archive, long-term retention)
  → ClickHouse (real-time fraud + analytics dashboards)
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design (PaymentIntent, Charge, PaymentMethod)
- Understands PCI-DSS: never store raw card data
- Basic state machine (created → processing → succeeded/failed)
- Webhook delivery for async status updates

### Senior
- Outbox pattern for safe card network calls
- Idempotency key to prevent double charges
- HSM/vault for card tokenization
- Authorization vs. capture two-phase flow

### Staff+
- Event sourcing for complete audit trail
- Kafka fan-out for webhooks + analytics
- DB sharding by merchant_id for 10K TPS
- Synchronous replication for zero data loss
- Fraud scoring pipeline integrated in hot path
- Detailed PCI-DSS compliance (network segmentation, HSM, key management)
