---
layout: simple
title: "Design a Payment System"
permalink: /system_design/design-payment-system
---

# Design a Payment System

A payment system handles the movement of money between parties in e-commerce transactions. It processes pay-in flows (receiving money from customers) and pay-out flows (sending money to sellers/merchants).

---

## Table of Contents

1. [Requirements](#requirements)
2. [Back of the Envelope Estimation](#back-of-the-envelope-estimation)
3. [High-Level Design](#high-level-design)
4. [API Design](#api-design)
5. [Database Design](#database-design)
6. [Payment Flow](#payment-flow)
7. [PSP Integration](#psp-integration)
8. [Deep Dive](#deep-dive)
9. [Handling Failures](#handling-failures)
10. [Reconciliation](#reconciliation)
11. [Security Considerations](#security-considerations)
12. [Key Takeaways](#key-takeaways)

---

## Requirements

### Functional Requirements

- **Pay-in flow**: Receive money from customers on behalf of sellers
- **Pay-out flow**: Send money to sellers worldwide
- **Payment tracking**: Track payment status through lifecycle
- **Multiple payment methods**: Support cards, bank transfers, digital wallets
- **Multi-currency support**: Handle international transactions

### Non-Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Reliability** | Handle failed payments gracefully with retry mechanisms |
| **Consistency** | Ensure exactly-once payment processing (no duplicate charges) |
| **Fault tolerance** | System continues operating during partial failures |
| **Reconciliation** | Internal records must match external PSP records |
| **Security** | PCI DSS compliance for handling card data |
| **Auditability** | Complete audit trail for all transactions |

### Extended Requirements

- Fraud detection and prevention
- Anti-money laundering (AML) compliance
- Real-time analytics and reporting
- Refund processing
- Dispute management

---

## Back of the Envelope Estimation

### Traffic Estimates

Assume an e-commerce platform with moderate scale:

```
Daily transactions: 1 million
Transactions per second: 1M / 86,400 = ~12 TPS (average)
Peak TPS: ~100 TPS (10x average during sales)
```

**Note**: Payment systems prioritize **correctness over throughput**. Unlike social media feeds, even 10 TPS requires extreme reliability.

### Storage Estimates

```
Transaction record size: ~1 KB
Daily transactions: 1 million
Daily storage: 1M × 1KB = 1 GB/day

Ledger entries (double-entry): 2 GB/day
Annual storage: ~1 TB/year

Keep 7 years for compliance: ~7 TB
```

### Summary

| Metric | Value |
|--------|-------|
| Average TPS | ~12 |
| Peak TPS | ~100 |
| Daily transactions | 1 million |
| Annual storage | ~1 TB |

---

## High-Level Design

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Client Applications                              │
│                         (Web, Mobile, Point of Sale)                          │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Load Balancer                                     │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Payment Service                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Risk Checker   │  │ Payment Router  │  │ Status Manager  │              │
│  │  (AML/Fraud)    │  │                 │  │                 │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  Payment Executor   │ │      Ledger         │ │      Wallet         │
│  (PSP Integration)  │ │  (Double-entry)     │ │  (Account Balance)  │
└──────────┬──────────┘ └─────────────────────┘ └─────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Payment Service Providers (PSPs)                           │
│     ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐               │
│     │ Stripe  │    │ PayPal  │    │  Adyen  │    │  Banks  │               │
│     └─────────┘    └─────────┘    └─────────┘    └─────────┘               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Responsibility |
|-----------|----------------|
| **Payment Service** | Accepts payment events, coordinates flow, performs risk checks |
| **Payment Executor** | Executes payment orders via PSPs |
| **PSP (Payment Service Provider)** | External service that moves money between accounts |
| **Ledger** | Financial transaction records using double-entry bookkeeping |
| **Wallet** | Tracks merchant account balances |
| **Risk Checker** | AML/CFT compliance and fraud detection |

---

## API Design

### Create Payment

```
POST /v1/payments
Content-Type: application/json
Idempotency-Key: unique-order-id-12345

Request:
{
    "buyer_info": {
        "id": "buyer_123",
        "email": "buyer@example.com"
    },
    "checkout_id": "checkout_abc",
    "credit_card_info": {
        "token": "psp_card_token_xyz"  // tokenized, never raw card data
    },
    "payment_orders": [
        {
            "seller_account": "seller_456",
            "amount": "99.99",
            "currency": "USD",
            "payment_order_id": "order_789"
        }
    ]
}

Response:
{
    "payment_id": "pay_abc123",
    "status": "PENDING",
    "created_at": "2024-01-15T10:30:00Z",
    "payment_orders": [
        {
            "payment_order_id": "order_789",
            "status": "PENDING",
            "amount": "99.99",
            "currency": "USD"
        }
    ]
}
```

### Get Payment Status

```
GET /v1/payments/{payment_id}

Response:
{
    "payment_id": "pay_abc123",
    "status": "COMPLETED",
    "payment_orders": [...],
    "executed_at": "2024-01-15T10:30:05Z"
}
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **String for amounts** | Avoid floating-point precision issues (e.g., "19.99" not 19.99) |
| **Idempotency key in header** | Prevent duplicate payments on retry |
| **Tokenized card data** | PSP handles raw card data, we only store tokens |

---

## Database Design

### Payment Event Table

```sql
CREATE TABLE payment_events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    payment_id VARCHAR(50) UNIQUE NOT NULL,
    buyer_id VARCHAR(50) NOT NULL,
    checkout_id VARCHAR(50) NOT NULL,
    amount DECIMAL(19, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'REFUNDED'),
    idempotency_key VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_buyer_id (buyer_id),
    INDEX idx_checkout_id (checkout_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);
```

### Payment Order Table

```sql
CREATE TABLE payment_orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    payment_order_id VARCHAR(50) UNIQUE NOT NULL,
    payment_event_id BIGINT NOT NULL,
    seller_account VARCHAR(50) NOT NULL,
    amount DECIMAL(19, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('PENDING', 'EXECUTING', 'SUCCESS', 'FAILED'),
    psp_reference VARCHAR(100),
    failure_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (payment_event_id) REFERENCES payment_events(id),
    INDEX idx_seller_account (seller_account),
    INDEX idx_psp_reference (psp_reference)
);
```

### Ledger Table (Double-Entry Bookkeeping)

```sql
CREATE TABLE ledger_entries (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    payment_order_id VARCHAR(50) NOT NULL,
    account_id VARCHAR(50) NOT NULL,
    entry_type ENUM('DEBIT', 'CREDIT') NOT NULL,
    amount DECIMAL(19, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    balance_after DECIMAL(19, 4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_payment_order (payment_order_id),
    INDEX idx_account (account_id),
    INDEX idx_created_at (created_at)
);
```

### Wallet Table

```sql
CREATE TABLE wallets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id VARCHAR(50) UNIQUE NOT NULL,
    account_type ENUM('BUYER', 'SELLER', 'PLATFORM'),
    balance DECIMAL(19, 4) NOT NULL DEFAULT 0,
    currency VARCHAR(3) NOT NULL,
    version INT NOT NULL DEFAULT 1,  -- optimistic locking
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_account_id (account_id)
);
```

### Double-Entry Bookkeeping Principle

**"Every transaction records both a debit and credit of equal amounts. The sum of all transaction entries must be 0."**

```
Transaction: Buyer pays $100 for product

┌─────────────────┬─────────────────┬─────────────────┐
│     Account     │      Debit      │     Credit      │
├─────────────────┼─────────────────┼─────────────────┤
│  Buyer Wallet   │     $100        │                 │
│  Seller Wallet  │                 │      $100       │
├─────────────────┼─────────────────┼─────────────────┤
│     Total       │     $100        │      $100       │
└─────────────────┴─────────────────┴─────────────────┘

Net = Debits - Credits = $100 - $100 = $0 ✓
```

---

## Payment Flow

### Pay-in Flow (Customer to Merchant)

```
┌──────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Client  │    │   Payment   │    │   Payment   │    │    PSP      │
│          │    │   Service   │    │   Executor  │    │  (Stripe)   │
└────┬─────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
     │                 │                  │                  │
     │  1. Place Order │                  │                  │
     │────────────────►│                  │                  │
     │                 │                  │                  │
     │                 │ 2. Store Event   │                  │
     │                 │─────────────────►│                  │
     │                 │      (DB)        │                  │
     │                 │                  │                  │
     │                 │ 3. Risk Check    │                  │
     │                 │◄────────────────►│                  │
     │                 │    (AML/Fraud)   │                  │
     │                 │                  │                  │
     │                 │ 4. Execute Order │                  │
     │                 │─────────────────►│                  │
     │                 │                  │                  │
     │                 │                  │ 5. Call PSP API  │
     │                 │                  │─────────────────►│
     │                 │                  │                  │
     │                 │                  │ 6. PSP Response  │
     │                 │                  │◄─────────────────│
     │                 │                  │                  │
     │                 │ 7. Update Wallet │                  │
     │                 │◄─────────────────│                  │
     │                 │                  │                  │
     │                 │ 8. Update Ledger │                  │
     │                 │◄─────────────────│                  │
     │                 │                  │                  │
     │ 9. Confirmation │                  │                  │
     │◄────────────────│                  │                  │
     │                 │                  │                  │
```

### Detailed Steps

1. **User clicks "Place Order"** - Payment event sent to Payment Service
2. **Store payment event** - Persist to database immediately
3. **Risk check** - Verify AML/CFT compliance, fraud detection
4. **Route to Payment Executor** - For each payment order in the event
5. **Execute via PSP** - Call external payment provider API
6. **Receive PSP response** - Success, failure, or pending
7. **Update wallet** - Adjust seller balance on success
8. **Record in ledger** - Create double-entry bookkeeping records
9. **Return confirmation** - Notify client of payment status

---

## PSP Integration

### Why Use a PSP?

| Direct Bank Connection | Using PSP |
|------------------------|-----------|
| Complex bank protocols | Simple REST APIs |
| Per-country integrations | Global coverage |
| Full PCI DSS compliance | Reduced compliance scope |
| Months of development | Days of integration |

### Hosted Payment Page Flow

```
┌──────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Client  │    │   Payment   │    │    PSP      │    │  PSP Hosted │
│  (Web)   │    │   Service   │    │   (Stripe)  │    │    Page     │
└────┬─────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
     │                 │                  │                  │
     │ 1. Checkout     │                  │                  │
     │────────────────►│                  │                  │
     │                 │                  │                  │
     │                 │ 2. Register      │                  │
     │                 │    Payment       │                  │
     │                 │─────────────────►│                  │
     │                 │                  │                  │
     │                 │ 3. Return Token  │                  │
     │                 │◄─────────────────│                  │
     │                 │                  │                  │
     │ 4. Redirect to  │                  │                  │
     │    PSP Page     │                  │                  │
     │◄────────────────│                  │                  │
     │                 │                  │                  │
     │ 5. Enter Card   │                  │                  │
     │─────────────────┼──────────────────┼─────────────────►│
     │                 │                  │                  │
     │                 │                  │ 6. Process Card  │
     │                 │                  │◄─────────────────│
     │                 │                  │                  │
     │ 7. Redirect to  │                  │                  │
     │    Success URL  │                  │                  │
     │◄────────────────┼──────────────────┼──────────────────│
     │                 │                  │                  │
     │                 │ 8. Webhook       │                  │
     │                 │    Notification  │                  │
     │                 │◄─────────────────│                  │
     │                 │                  │                  │
```

### Benefits of Hosted Page

- **Card data never touches your servers** - Reduced PCI DSS scope
- **PSP handles 3D Secure** - Built-in fraud prevention
- **Consistent UX** - Trusted payment form
- **Automatic compliance** - PSP maintains security certifications

---

## Deep Dive

### Idempotency

**Problem**: Network failures can cause duplicate payment requests.

```
Client ──► Payment Service ──► PSP
              │
              │ Timeout (but PSP processed it!)
              │
Client ──► Retry ──► Duplicate charge!
```

**Solution**: Idempotency key in HTTP header

```
POST /v1/payments
Idempotency-Key: order_123_attempt_1

First request:  Process payment, store result with key
Second request: Return cached result (no reprocessing)
```

### Implementation

```python
def process_payment(idempotency_key, payment_request):
    # Check if already processed
    existing = db.get_by_idempotency_key(idempotency_key)
    if existing:
        return existing.result  # Return cached result

    # Process new payment
    result = execute_payment(payment_request)

    # Store with idempotency key
    db.save(idempotency_key, result)

    return result
```

### Database Constraint

```sql
CREATE UNIQUE INDEX idx_idempotency ON payment_events(idempotency_key);
```

### Exactly-Once Delivery

Achieved through two guarantees:

```
┌─────────────────────────────────────────────────────────────┐
│                    Exactly-Once Delivery                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   At-Least-Once (Retry)    +    At-Most-Once (Idempotency)  │
│                                                              │
│   ┌─────────────────┐         ┌─────────────────┐           │
│   │ Keep retrying   │    +    │ Idempotency key │           │
│   │ until success   │         │ prevents dupes  │           │
│   └─────────────────┘         └─────────────────┘           │
│                                                              │
│   = Exactly-Once Semantics                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Communication Patterns

**Synchronous (REST/HTTP)**

```
Payment Service ──HTTP──► PSP
        │
        │ Wait for response
        ▼
     Continue
```

- **Pros**: Simple, immediate feedback
- **Cons**: Tight coupling, poor failure isolation

**Asynchronous (Message Queue)**

```
Payment Service ──► Kafka ──► Payment Executor ──► PSP
                     │
                     └───► Analytics
                     │
                     └───► Billing
```

- **Pros**: Loose coupling, better scalability
- **Cons**: Eventual consistency, complexity

### Choosing Between Sync and Async

| Scenario | Recommendation |
|----------|----------------|
| Low volume (<100 TPS) | Synchronous |
| High volume (>1000 TPS) | Asynchronous |
| Real-time confirmation needed | Synchronous |
| Multiple downstream consumers | Asynchronous |

---

## Handling Failures

### Types of Failures

| Failure Type | Example | Retry? |
|--------------|---------|--------|
| **Transient** | Network timeout, 503 | Yes |
| **Permanent** | Invalid card, insufficient funds | No |
| **Unknown** | No response, 500 | Yes (with caution) |

### Retry Strategies

```
┌─────────────────────────────────────────────────────────────┐
│                     Retry Strategies                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Immediate Retry                                          │
│     [Attempt 1] ─► [Attempt 2] ─► [Attempt 3]               │
│                                                              │
│  2. Fixed Interval                                           │
│     [Attempt 1] ─5s─► [Attempt 2] ─5s─► [Attempt 3]         │
│                                                              │
│  3. Incremental Interval                                     │
│     [Attempt 1] ─5s─► [Attempt 2] ─10s─► [Attempt 3]        │
│                                                              │
│  4. Exponential Backoff (Recommended)                        │
│     [Attempt 1] ─1s─► [Attempt 2] ─2s─► [Attempt 3] ─4s─►   │
│                                                              │
│  5. Cancel (Permanent failure)                               │
│     [Attempt 1] ─► [Mark as failed]                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Queue Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Retry Queue System                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐      ┌─────────────┐      ┌────────────┐  │
│   │   Payment   │      │   Retry     │      │   Dead     │  │
│   │   Queue     │ ───► │   Queue     │ ───► │   Letter   │  │
│   │             │      │ (3 retries) │      │   Queue    │  │
│   └─────────────┘      └─────────────┘      └────────────┘  │
│                                                              │
│   Normal flow          Transient errors     Needs manual    │
│                        auto-retry           investigation   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Implementation

```python
class PaymentExecutor:
    MAX_RETRIES = 3

    def execute_with_retry(self, payment_order):
        for attempt in range(self.MAX_RETRIES):
            try:
                result = self.psp.charge(payment_order)

                if result.is_success():
                    return result

                if result.is_permanent_failure():
                    # Don't retry permanent failures
                    return result

            except NetworkError:
                delay = 2 ** attempt  # Exponential backoff
                time.sleep(delay)

        # Move to dead letter queue after max retries
        self.dead_letter_queue.send(payment_order)
        raise PaymentFailedError("Max retries exceeded")
```

---

## Reconciliation

### Why Reconciliation?

**"The last line of defense"** - Even with idempotency and retry logic, discrepancies can occur:

- PSP processed but webhook failed
- Internal system recorded but PSP didn't process
- Amount mismatch due to currency conversion
- Timing differences between systems

### Reconciliation Process

```
┌─────────────────────────────────────────────────────────────┐
│                   Daily Reconciliation                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐                 ┌─────────────┐           │
│   │   Internal  │                 │ PSP Settlement│          │
│   │   Ledger    │                 │   File        │          │
│   └──────┬──────┘                 └──────┬───────┘          │
│          │                               │                   │
│          └───────────┬───────────────────┘                  │
│                      │                                       │
│                      ▼                                       │
│              ┌──────────────┐                                │
│              │   Compare    │                                │
│              │  & Match     │                                │
│              └──────┬───────┘                                │
│                     │                                        │
│        ┌────────────┼────────────┐                          │
│        ▼            ▼            ▼                          │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│   │ Matched │  │Mismatch │  │ Missing │                    │
│   │   OK    │  │ (Diff)  │  │ (One-   │                    │
│   │         │  │         │  │ sided)  │                    │
│   └─────────┘  └────┬────┘  └────┬────┘                    │
│                     │            │                          │
│                     ▼            ▼                          │
│              ┌───────────────────────┐                      │
│              │   Resolution Queue    │                      │
│              │                       │                      │
│              │ - Auto-fix (known)    │                      │
│              │ - Manual review       │                      │
│              │ - Investigation       │                      │
│              └───────────────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Mismatch Categories

| Category | Example | Resolution |
|----------|---------|------------|
| **Timing** | PSP settled next day | Auto-match next cycle |
| **Amount** | Currency conversion diff | Auto-fix if < threshold |
| **Missing internal** | Webhook failed | Auto-create from PSP data |
| **Missing external** | PSP didn't process | Investigate, refund if needed |
| **Status mismatch** | Internal=success, PSP=failed | Manual investigation |

### Implementation

```python
class ReconciliationService:
    def daily_reconciliation(self, date):
        # Get internal records
        internal_records = self.ledger.get_by_date(date)

        # Get PSP settlement file
        psp_records = self.psp.get_settlement_file(date)

        # Match records
        matched, mismatched, missing = self.match_records(
            internal_records,
            psp_records
        )

        # Process mismatches
        for mismatch in mismatched:
            if self.can_auto_fix(mismatch):
                self.auto_fix(mismatch)
            elif self.is_classifiable(mismatch):
                self.manual_queue.add(mismatch)
            else:
                self.investigation_queue.add(mismatch)

        return ReconciliationReport(matched, mismatched, missing)
```

---

## Security Considerations

### PCI DSS Compliance

**Payment Card Industry Data Security Standard** - Required for handling card data

| SAQ Level | Description | Requirements |
|-----------|-------------|--------------|
| **SAQ A** | Hosted payment page | Minimal (outsourced to PSP) |
| **SAQ A-EP** | iFrame integration | More controls |
| **SAQ D** | Direct card handling | Full compliance (~300 controls) |

**Recommendation**: Use hosted payment page (SAQ A) unless you have specific requirements.

### Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Network Security                                   │
│  ├── TLS 1.3 for all communications                         │
│  ├── WAF (Web Application Firewall)                         │
│  └── DDoS protection                                        │
│                                                              │
│  Layer 2: Application Security                               │
│  ├── Input validation                                       │
│  ├── Rate limiting                                          │
│  └── Request signing (HMAC)                                 │
│                                                              │
│  Layer 3: Data Security                                      │
│  ├── Encryption at rest (AES-256)                          │
│  ├── Tokenization (no raw card data)                       │
│  └── Data masking in logs                                   │
│                                                              │
│  Layer 4: Fraud Prevention                                   │
│  ├── 3D Secure                                              │
│  ├── Velocity checks                                        │
│  ├── Device fingerprinting                                  │
│  └── ML-based fraud detection                               │
│                                                              │
│  Layer 5: Compliance                                         │
│  ├── AML/KYC checks                                         │
│  ├── Sanctions screening                                    │
│  └── Audit logging                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Rate Limiting

```python
from redis import Redis
import time

class PaymentRateLimiter:
    def __init__(self, redis):
        self.redis = redis

    def check_rate_limit(self, buyer_id, card_hash):
        """Prevent card testing attacks"""

        # Limit per buyer: 10 payments per hour
        buyer_key = f"rate:buyer:{buyer_id}:{int(time.time() // 3600)}"
        if self.redis.incr(buyer_key) > 10:
            raise RateLimitError("Too many payment attempts")
        self.redis.expire(buyer_key, 3600)

        # Limit per card: 5 payments per hour
        card_key = f"rate:card:{card_hash}:{int(time.time() // 3600)}"
        if self.redis.incr(card_key) > 5:
            raise RateLimitError("Card rate limit exceeded")
        self.redis.expire(card_key, 3600)
```

### Fraud Detection Signals

| Signal | Description | Risk Level |
|--------|-------------|------------|
| Velocity | Many transactions in short time | High |
| Geolocation | IP location vs billing address | Medium |
| Device | New device, browser fingerprint | Medium |
| Amount | Unusually large transaction | Medium |
| Time | Odd hours (3 AM local time) | Low |
| Behavior | Cart abandonment pattern | Low |

---

## Data Consistency

### Challenges

- Multiple databases (payment, ledger, wallet)
- External PSP state
- Network partitions

### Approaches

**Option 1: Single Primary Database**

```
┌─────────────┐
│   Primary   │ ◄── All reads/writes
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Replicas   │ ◄── Async replication
│  (Read-only)│
└─────────────┘
```

- **Pros**: Strong consistency, simple
- **Cons**: Limited scalability

**Option 2: Distributed Database (Recommended for scale)**

```
┌─────────────────────────────────────────────────────────────┐
│         Distributed Database (CockroachDB/YugabyteDB)        │
│                                                              │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│   │  Node 1 │◄──►│  Node 2 │◄──►│  Node 3 │                │
│   │  (Raft) │    │  (Raft) │    │  (Raft) │                │
│   └─────────┘    └─────────┘    └─────────┘                │
│                                                              │
│   Consensus-based replication (Raft/Paxos)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

- **Pros**: Horizontal scale, strong consistency
- **Cons**: Complexity, latency overhead

### Handling PSP Sync

```python
def execute_payment_safely(payment_order):
    # 1. Create pending record
    payment_order.status = 'PENDING'
    db.save(payment_order)

    try:
        # 2. Call PSP
        psp_result = psp.charge(payment_order)

        # 3. Update based on PSP result
        payment_order.status = psp_result.status
        payment_order.psp_reference = psp_result.reference
        db.save(payment_order)

        # 4. Update ledger and wallet
        if psp_result.is_success():
            ledger.record(payment_order)
            wallet.update_balance(payment_order.seller, payment_order.amount)

    except Exception as e:
        # 5. Mark for reconciliation
        payment_order.status = 'UNKNOWN'
        payment_order.error = str(e)
        db.save(payment_order)
        reconciliation_queue.add(payment_order)
```

---

## Key Takeaways

### 1. Correctness Over Performance

Payment systems prioritize **correctness** over throughput. Even at 10 TPS, reliability is paramount.

### 2. Double-Entry Bookkeeping

Every transaction must have balanced debits and credits. This ensures:
- Audit trail
- Error detection
- Regulatory compliance

### 3. Idempotency is Critical

Use idempotency keys to prevent duplicate charges:
- Store with unique constraint
- Return cached result on duplicate request

### 4. PSP Integration Strategy

Use hosted payment pages when possible:
- Reduced PCI scope
- Built-in security features
- Faster time to market

### 5. Defense in Depth

```
┌─────────────────────────────────────────────────────────────┐
│                   Payment Defense Layers                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Layer 1: Idempotency      ─► Prevent duplicates           │
│   Layer 2: Retry with backoff─► Handle transient failures   │
│   Layer 3: Dead letter queue ─► Capture unresolvable cases │
│   Layer 4: Reconciliation    ─► Catch everything else       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6. Production Checklist

- [ ] Idempotency key handling
- [ ] Retry with exponential backoff
- [ ] Dead letter queue for failures
- [ ] Daily reconciliation process
- [ ] Double-entry ledger
- [ ] Rate limiting
- [ ] Fraud detection
- [ ] PCI compliance (use hosted page)
- [ ] AML/KYC checks
- [ ] Comprehensive logging and monitoring

### 7. Interview Discussion Points

1. **Why double-entry bookkeeping?** Ensures data integrity, audit trail, error detection
2. **Sync vs Async communication?** Trade-off between simplicity and scalability
3. **How to handle partial failures?** Idempotency + retry + reconciliation
4. **Why use PSP instead of direct bank?** Complexity, compliance, global coverage
5. **How to ensure exactly-once delivery?** At-least-once (retry) + at-most-once (idempotency)
6. **Reconciliation frequency?** Daily minimum, hourly for high-volume
7. **How to handle currency conversion?** Store original + converted amounts, reconcile differences

### 8. Trade-offs Summary

| Decision | Option A | Option B |
|----------|----------|----------|
| Communication | Sync (simple) | Async (scalable) |
| Card handling | Direct (control) | Hosted page (compliant) |
| Database | Single (consistent) | Distributed (scalable) |
| Retry | Immediate (fast) | Backoff (reliable) |
| Reconciliation | Real-time (expensive) | Batch (efficient) |

---

## References

- [Designing a Payment System - Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/designing-a-payment-system)
- System Design Interview Volume 2 - Alex Xu
- PCI DSS Documentation
- Stripe/PayPal API Documentation
