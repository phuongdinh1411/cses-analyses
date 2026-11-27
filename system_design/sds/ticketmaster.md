---
layout: simple
title: "Design Ticketmaster — System Design School"
permalink: /system_design/sds/ticketmaster
---

# Design Ticketmaster

**Difficulty:** Hard  
**Topics:** Consistency · Reservation holds · Waiting room · Rate limiting · Async processing

## Summary

- **Key challenge:** Never sell a seat twice while ~1M buyers stampede 50K seats in the first minute (~20 contenders per seat).
- **Core design:** A waiting room admits users with tokens; browsing reads a cache; a hold is an expiring in-memory key; purchase charges payment, then runs one conditional write in a strongly consistent seat DB.
- **Techniques:** SET NX EX hold (one winner, auto-expiry); 409 to losers (fail fast); conditional UPDATE WHERE status='available' (final oversell guard); waiting room with signed admission token (absorbs spike); idempotent reserve-charge-confirm saga (survives payment failures, crashes).

## Ticketmaster and ticket booking system design problem statement

Design a system that sells tickets to events with assigned seats: users browse what's available, pick a seat, and buy it. The same seat must never sell twice.

In scope: browsing seat availability, holding a seat during checkout, purchasing a held seat, and releasing an expired or abandoned hold. Out of scope: dynamic pricing, seat recommendations, and the internals of the payment provider itself.

## Ticket booking system design interview questions

Each answer fixes an assumption the design leans on.

- Assigned seats or general admission? Assigned seats — the hard case, where each seat is a unique unit of inventory. General admission, a single counter per tier, is a variant.

- How spiky is demand? Extremely. A hot on-sale sells out in minutes with far more buyers than seats, which is what makes contention the central problem, not average load.

- Is overselling ever acceptable? No. Selling one seat twice is a correctness failure, so inventory is strongly consistent even at the cost of availability.

- How long does a hold last? A few minutes — long enough to check out, short enough that an abandoned cart returns to inventory quickly.

- Are payments in scope? No. Checkout hands off to an existing payment system; this design focuses on inventory and the on-sale stampede.

## What makes this problem distinctive

The difficulty isn't browsing. It's that a popular on-sale is a synchronized stampede — on the order of a hundred thousand people trying to grab the same few thousand seats in the same few seconds — and inventory correctness must hold exactly under that contention.

A naive "mark the seat sold on click" design fails in two directions at once. Read it as one operation and two clicks on the same seat both succeed, selling it twice. Slow it down with a lock held until checkout completes and one abandoned cart freezes a seat forever. The system needs a temporary, expiring reservation — a hold — that lets exactly one buyer through per seat, and a way to absorb a hundred-thousand-person spike without the inventory service failing under the load.

Key idea. A popular on-sale is a synchronized stampede against a small, fixed inventory — the design needs exactly one winner per seat and a way to survive the spike that produces that winner.

## Key concepts

This section covers the concepts needed to solve this problem — prerequisites for the design work that follows.

### The hold

A hold is a short-lived reservation on a seat. It locks the seat for one buyer during checkout, and it expires by itself if the buyer does not pay in time. The hold separates "reserved" from "sold," and its expiry keeps an abandoned cart from stranding a seat.

A hold is temporary state, so it does not have to live in the database of record. A common design keeps each hold as a key in an in-memory store, a key-value store that keeps its data in RAM, with an expiry set on the key. When the expiry passes, the store deletes the key, and the seat is free again. Only a completed purchase writes to the database, where the seat changes from available to sold.

### Atomic compare-and-set

A hold must be claimed in one indivisible step: claim the seat only if nobody else holds it. If a request reads "free" and then writes "held" in a second step, two requests can both read "free" before either one writes. When a thousand requests race for the same seat, the store must process the check and the write together, so that one request wins and the others fail.

Compare-and-set (CAS). A conditional write: "set X to value B, but only if X currently equals A." If another writer changed X first, the CAS fails cleanly instead of overwriting a change it never saw.

The design uses CAS in two forms. In the in-memory store, the hold is a set-if-absent: "create this key only if it does not exist." This is a CAS where the expected value is "absent." For example, in Redis the command SET hold:{event}:{seat} {user_id} NX EX 600 creates the key with a 600-second expiry only if the key is absent. The first request gets OK, and each later request gets no result. In the database, the sale is a conditional update: UPDATE seats SET status='sold' WHERE id=? AND status='available'. The first update changes one row, and a later update changes zero rows.

### The waiting room

A virtual queue issues each arriving user a token and admits them into the buying flow at a rate the inventory service can handle. It turns a simultaneous wall of demand into a controlled stream. This is the same throttling idea behind rate limiting, applied to an entire on-sale event rather than a per-client quota. Despite the name, the virtual queue is not a message queue. It is an in-memory store that keeps each user's token and position, for example a sorted set keyed by arrival time, and the system admits users from the front of that order.

The waiting room covers specific routes, not the whole site. The routing layer in front of the app servers (a load balancer, an API gateway, or the CDN edge) checks each request. Search, concert pages, and account pages go straight to the app servers as usual. Requests for the hot event's buying flow (the seat map, holds, checkout) that carry no admission token go to the waiting room instead. The waiting room is its own small service: it serves the "you are number 40,000 in line" page and keeps the line, so a million people refreshing a waiting page never load the booking servers. This is how hosted waiting rooms work. Cloudflare Waiting Room is configured for chosen routes and serves the waiting page from Cloudflare's edge before requests reach the origin. Queue-it redirects visitors without a token to a waiting room on its own servers with an HTTP 302 and sends them back with a token in order. The AWS Virtual Waiting Room runs the line behind its own endpoints and issues tokens that let users into the protected site in controlled waves.

When a user's turn comes, the waiting room issues a short-lived admission token, usually as a cookie. The routing layer lets requests that carry a valid token through to the app servers, and the booking API checks the token again before it accepts a hold, so a user cannot skip the line by calling the booking API directly. Admission does not reserve a seat. It only controls the rate at which buyers reach the inventory service.

### Cached browse, fast hold, consistent sale

Browsing, holding, and buying have different consistency needs, and the design gives each one a different store. Availability views come from an eventually consistent cache. A stale view at worst shows a seat that was just taken, and the hold catches that when the user tries to claim the seat. The hold goes to the in-memory store, which gives fast claims and a built-in expiry. The sale is the one write that must be exactly correct, so it goes to a strongly consistent database as a conditional update.

Key idea. A hold is a temporary, expiring reservation kept in an in-memory store; set-if-absent and the conditional update are two forms of compare-and-set that let one contender win; a waiting room throttles the stampede and issues the token the booking API checks; and only the final sale needs a strongly consistent write.

## 1. Requirements

Before reading on. List the functional and non-functional requirements, then name the one property you would never compromise and the one constraint that drives the design.

### 1.1 Functional requirements

- Browse availability — which seats are open for an event.

- Hold a seat — temporarily reserve it while checking out.

- Purchase a held seat, converting the hold into a sale via the payment system.

- Release — holds expire and return to inventory automatically.

### 1.2 Non-functional requirements

- No overselling. A seat sells once. The final conditional write at purchase enforces this — the dominating correctness requirement.

- Fairness under spike. The on-sale stampede is admitted in a controlled, roughly-fair order.

- Low-latency hold. Grabbing a seat feels instant even under load, which is why the hold is an in-memory operation.

- Available browsing. The read path stays up and fast even while the write path is under heavy contention.

### 1.3 The constraint versus the property

The property never to compromise is no overselling: a seat sells once, no matter how many simultaneous requests race for it. The constraint that drives the design is that this has to hold under a stampede far larger than the inventory itself. The design splits the work. The in-memory hold gives fast, fair claims and absorbs the contention. One conditional write in a strongly consistent database at purchase enforces the property. Everything else, browsing included, stays as available and cheap as possible.

Key idea. No overselling is the property that can't bend; surviving a demand spike that dwarfs supply, without bending it, is the constraint the rest of the design answers.

## 2. Back-of-the-envelope estimation

Seats for sale50K

Buyers in the first minute1.0M

Browse reads per hold attempt200:1

Contenders per seat

20×

1.0M buyers ÷ 50K seats

Hold attempts / sec

17K/s

bounded by seat count, small in absolute terms

Browse reads / sec

3.3M/s

orders of magnitude above hold attempts

What must be exact

the hold

a small, atomic write path — not the read volume

1.0M buyers ÷ 50K seats ≈ 20× contenders per seat — the crush the design exists to resolve

Reads (browsing) dwarf writes (holds) — holds are capped by seat count. The read path scales with caching; the hold path must be small and exactly correct.

### 2.1 Demand dwarfs supply

Assume a 50,000-seat venue with about 1,000,000 buyers arriving in the first minute of an on-sale. That's 1,000,000 ÷ 50,000 = 20 contenders per seat — the contention the entire design exists to resolve correctly.

### 2.2 Reads overwhelm writes

Browsing is orders of magnitude more frequent than holds. Holds are bounded by the seat count: no more than 50,000 seats can be on hold at any instant in a 50,000-seat venue. Expired holds re-issue, so total holds over the whole sale exceed that, but the concurrent bound stays fixed. Hold attempts land on the in-memory store, not the database. The database sees roughly one conditional write per sold seat, at most 50,000 for the venue. The read path scales independently through caching; the write path is small in volume but has to be exactly correct.

### 2.3 The write hotspot is per-seat

Contention doesn't spread evenly across the venue — it concentrates on the good seats. The unit of serialization is one seat, and the hottest seats are the entire problem. Sharding by event does nothing for contention that lands on a single hold key within that event.

Key idea. The 20-to-1 (or worse) contenders-per-seat ratio, not the raw request volume, is the number that sizes this system — and it lands unevenly, on individual hot seats.

## 3. API design

Design checkpoint

A thousand requests arrive for the same seat in the same millisecond. What must the hold endpoint return to the losers that a normal write wouldn't need to?

A generic 500 error, retried by the clientAn explicit 409 (already taken), so the client can immediately show the seat as gone

### 3.1 Browse availability

GET/v1/events/{id}/seats

Request & response

Served from the eventually consistent availability cache for sold seats, plus the in-memory store's list of held seats for the event. This is the high-volume read path.

### 3.2 Hold a seat

POST/v1/events/{id}/holds

Request & response

The user comes from the authenticated session, and the admission token from the waiting room goes in a request header. The booking API rejects a request without a valid admission token. It then runs set-if-absent with an expiry on each seat's hold key. A losing request gets 409 immediately — no queueing, no retry-and-hope. For a request with several seats, a short script in the in-memory store sets all the keys or none, so a buyer does not end up with half a row of seats.

### 3.3 Purchase a held seat

POST/v1/holds/{id}/purchase

Request & response

The booking API first checks that the hold key still contains this user's id, then charges the payment, then runs the conditional update in the database. It returns 410 if the hold expired, or if the conditional write finds the seat already sold. 410 (rather than 409) signals that this buyer's claim lapsed, distinct from another buyer winning the seat at hold time.

Key idea. The hold endpoint is a set-if-absent that fails fast and explicitly — losers get 409 immediately — and the purchase endpoint re-checks the claim with a conditional write before it confirms a sale.

## 4. Data model

### 4.1 Seat

The unit of inventory — one row per physical seat, in the database. Its status has two values, available and sold. A hold does not change this row.

### 4.2 Hold

A temporary, time-bounded claim on a seat. It is an in-memory record, not a database row: the key names the seat, the value is the user's id, and the key's expiry is the hold's lifetime.

The key has the form hold:{event_id}:{seat_id}. To draw held seats on the seat map, the store also keeps a per-event sorted set of held seats, scored by expiry time. A seat map read gets the event's held seats in one call and ignores entries whose score is already in the past.

### 4.3 Order

The record of a completed purchase.

### 4.4 Where each entity lives

Seat rows live in a strongly consistent, transactional database, partitioned by event_id. The available → sold transition is a single conditional update against this database. Order rows are written in the same transaction as that update, on successful purchase. Hold records live in the in-memory store, and the key expiry enforces the hold's lifetime, so no sweeper job is needed. The availability shown to browsers is a separate, read-only, eventually consistent cache derived from Seat — never the system of record.

Key idea. Seat, Hold, and Order form one lifecycle — available → held → sold — but they live in different stores: the hold in memory, where it can expire for free, and the sale in the strongly consistent database, the only place the lifecycle's correctness is enforced.

## 5. Ticket booking system architecture and high-level design

Before reading on. You already have the hold, atomic compare-and-set, the waiting room, and the cache/consistency split from Key concepts. Sketch what happens from "user clicks a seat" to "seat is sold," and where each of those four mechanisms plugs in.

### 5.1 Mark the seat sold on click

Start naive: the user picks a seat, and the server marks it sold directly.

Four things break this at scale.

- Two users click the same seat close together and both get marked sold, overselling it.

- A user who holds a seat and abandons the page leaves it stuck forever — nothing ever frees it.

- A hundred thousand users hitting the service at the same instant overwhelms it outright.

- Everyone refreshing availability at once hammers the same database the sale itself needs.

### 5.2 Fix 1: an atomic hold in an in-memory store

Split "sell" into hold-then-buy. The hold is a set-if-absent on the seat's key in an in-memory store, for example SET hold:{event}:{seat} {user_id} NX. The first request creates the key and wins. Each later request finds the key present and gets 409. The race now plays out in memory, and the database is not involved until purchase.

Two clicks on the same seat no longer both win. An abandoned hold still strands the seat, and the service still has no defense against a hundred-thousand-person spike.

### 5.3 Fix 2: a hold expiry and a final write at purchase

Add an expiry to the same command: SET hold:{event}:{seat} {user_id} NX EX 600. The key deletes itself 600 seconds after it is set, so an abandoned hold returns the seat to inventory with no sweeper job.

The hold now lives in a different store from the sale, and that creates a new failure. An in-memory store can lose a key, for example when a primary fails over before it copies the key to a replica, or when the store evicts keys under memory pressure. A second buyer can then hold the same seat, and two buyers can both reach payment. So the purchase does not trust the hold alone. It checks that the hold key still contains this user's id, and after payment succeeds it runs one conditional write in the database: UPDATE seats SET status='sold', order_id=? WHERE id=? AND status='available'. If the two buyers both pay, only one update changes a row. The other buyer is refunded and the hold is released.

Abandoned holds no longer strand seats, and a lost hold key cannot produce a double sale. The service still has to survive the initial stampede of arrivals.

### 5.4 Fix 3: a waiting room

The routing layer (the load balancer or the CDN edge) sends requests for the hot event's buying flow that have no admission token to a waiting room service. Everything else, such as search and concert pages, still goes straight to the app servers. The waiting room serves its own waiting page and keeps each user's token and position in an in-memory store, for example a sorted set keyed by arrival time. It admits users in batches at a rate the downstream systems can handle and gives each admitted user a short-lived admission token. Requests with a valid token pass through to the booking API, which checks the token again before it accepts a hold.

The service survives the on-sale moment. Every admitted user still hammers the same database just to see what's available.

### 5.5 Fix 4: a cached browse path

Availability is served from an eventually consistent cache, so the flood of "what's open?" reads does not touch the transactional database. The cache holds sold seats, derived from the Seat DB. Held seats come from the in-memory store's per-event sorted set, so the seat map shows a seat as taken as soon as someone holds it.

### 5.6 The composed design

Each component answers one failure of the naive version. The in-memory hold stops two clicks from both claiming a seat. Its expiry frees stranded seats. The conditional write at purchase is the final guard against an oversell when the hold store loses a key. The waiting room stops the stampede from overwhelming the service, and the cached browse path keeps read traffic off the consistent database.

### 5.7 Sequence: browse, hold, and purchase

Key idea. Browsing, holding, and buying are different consistency guarantees living side by side: a stale browse view at worst causes a 409 that the hold catches, and a lost hold at worst causes a refund that the conditional write catches, so neither cache staleness nor a lost hold key can cause an oversell.

## 6. Deep dives

### 6.1 The hold and no oversell

Before reading on. A thousand requests try to hold seat 14A in the same millisecond. One must win. What's the primitive, where does the contention actually land, and what still protects the sale if the hold is lost?

The hold is a set-if-absent with an expiry in the in-memory store: SET hold:{event}:{seat} {user_id} NX EX 600. The store processes commands on a key one at a time, and it runs the existence check, the write, and the expiry as one atomic command (Redis SET docs). The first request gets OK, and every other request gets no result and receives 409. The expiry releases abandoned holds, so the design needs no sweeper for holds. This keeps the race off the database and makes each claim a fast in-memory operation.

The widget runs the same race in its database form, a conditional UPDATE. The set-if-absent behaves the same way: requests on one key are serialized, the first one wins, and each later one finds the claim already taken.

Race for one seatHold expires, seat reopens

Play Step Reset

t0 — 5 requests arrive in the same millisecond

seat 14A status

available

Alice

pending

Bob

pending

Carol

pending

Dave

pending

Eve

pending

All five contenders send POST /events/{id}/holds for seat 14A at once.

Contention concentrates on individual hot seats, not the event as a whole — front-row seats absorb the fight while back rows sit uncontested. Sharding the whole event across nodes doesn't help a single hot key; the seat still needs one serialized decision, so the main lever is making that decision as cheap as possible. An in-memory set-if-absent is cheap. Per-seat request queues or a best-available allocation mode can spread the contention, but they don't remove the serialization.

Design checkpoint

The in-memory store fails over and loses Alice's hold on seat 14A. Bob then holds 14A, and both Alice and Bob reach payment. What stops the seat from selling twice?

Nothing — the hold is the only check, so the seat sells twiceThe conditional write at purchase: only one UPDATE ... WHERE status = 'available' changes the row, and the other buyer is refunded

The hold gives fast, fair claims, but it is not the final guard. An in-memory store can lose a key: a primary can fail over before it copies a recent write to its replica, and a store under memory pressure can evict keys. If Alice's key disappears, Bob can hold the same seat, and both can pay. The purchase therefore makes two checks. Before it charges, it reads the hold key and confirms that the value is this user's id. After payment succeeds, it runs UPDATE seats SET status='sold', order_id=? WHERE id=? AND status='available' in the strongly consistent database. In the lost-key case, both checks can pass for both buyers, but only one update changes a row. The other buyer's update changes zero rows, so that charge is refunded and that hold is released. Setting the store's eviction policy so that hold keys are not evicted makes this case rarer, but the conditional write is what closes it.

The alternative keeps the hold in the database. The hold is a conditional update from available to held, with an expires_at column. A background job sweeps expired holds, or the hold path checks expires_at on read and treats an expired hold as available. This design has one strongly consistent source of truth, with no second store to keep in agreement. The cost is that every hold attempt is a write to the database, and hot seats concentrate row contention there, during the busiest seconds of the sale. The in-memory design keeps that contention off the database and gets expiry for free. Its cost is two stores that must agree, which is why the purchase write re-checks the seat status.

What to monitor: any seat that ends up in two orders (an oversell, which the conditional write should prevent), the rate of zero-row purchase writes (each one is a lost hold and a refund), and the held-but-never-purchased rate (abandoned-cart volume).

What separates answers — the hold and no oversell

BadRead status, then write sold separately▾

GoodAn atomic hold with an expiry▾

GreatIn-memory hold, final conditional write, and the trade-off against a DB-only hold▾

### 6.2 The waiting room

Before reading on. A million people hit "buy" at 10:00:00 sharp. If they all reach the inventory service at once, it dies. How do you let them in without dropping the correctness guarantee?

The waiting room covers the hot event's buying routes only. The routing layer sends buy-flow requests without an admission token to the waiting room service, which serves the waiting page; search and concert pages keep going straight to the app servers. Arrivals receive a queue token and a position in an in-memory store, for example a sorted set keyed by arrival time. The system admits users from the front of that order in batches, at a rate the inventory service can absorb. This is the same throttling idea as rate limiting, applied to an entire event's on-sale rather than one client's quota. Each admitted user is notified with a push over a persistent connection or a redirect back to the site, and receives a short-lived admission token. Hosted waiting rooms work this way: Cloudflare Waiting Room serves the waiting page from its edge for the routes it is configured on, Queue-it redirects visitors without a token to a waiting room on its own servers and sends them back in order, and the AWS Virtual Waiting Room issues tokens so users enter in controlled waves.

The booking API checks the admission token before it accepts a hold request. Without that check, a user could skip the queue by sending hold requests to the booking API directly. The token is short-lived and tied to the user and the event, so it cannot be reused later or shared across many accounts. The booking API can verify a signed token without a call to the waiting room, which keeps the check cheap on the hold path.

Position is roughly ordered by arrival, which is fairer than "whoever's retry lands first wins." Perfect fairness at this scale isn't achievable — network jitter alone means two people who clicked at the same instant can arrive in either order — but roughly-ordered admission is the realistic, defensible bar. Being admitted does not reserve a seat: inventory can sell out while someone is still queuing, so the client has to handle "your turn, but it's gone" as a normal outcome, not an error. The waiting room protects the inventory service and smooths the spike. Without one, a hot on-sale can overwhelm the inventory service the same way an external denial-of-service attack would. What to monitor: admit rate against inventory-service latency (back off admission as latency climbs), queue depth, abandonment, and the rate of hold requests rejected for a missing or expired token.

Design checkpoint

A user is admitted from the waiting room, but the seat they wanted just sold out. Whose bug is this?

A bug in the waiting room — it should have reserved the seatNot a bug — the waiting room only throttles arrivals, it never guarantees availability

What separates answers — the waiting room

BadNo queue at all▾

GoodA virtual queue admitting at a fixed rate▾

GreatArrival-ordered fairness, admission token, adaptive rate, explicit no-guarantee▾

### 6.3 The purchase-to-payment seam

Before reading on. A user has a hold and clicks buy, but their card is declined. What must happen to the seat? And what if payment succeeds but your service crashes before recording the order?

The hold reserves the seat for this user, so payment can take its time — up to the hold's expiry — without another buyer sneaking in, the ticketing equivalent of a payment authorization holding funds before they're captured. Converting a hold to a sale is a small saga: reserve (the in-memory hold) → charge (payment) → confirm (the conditional write that marks the seat sold and writes the order). If payment succeeds and the conditional write changes one row, the order is confirmed. If payment is declined, the compensation is releasing the hold. The booking API can delete the hold key, checking first that its value is still this user's id, or it can let the key expire. A charge that succeeds after the hold has lapsed is the awkward case. The confirm step re-checks the hold key, and the conditional write re-checks the seat status. If either check fails, the charge is voided or refunded rather than selling a seat that someone else now holds or owns.

The remaining gap is a crash between a successful charge and a recorded order. Both steps carry an idempotency key derived from the hold: the payment system dedups a retried charge, and a retried confirmation finalizes the same outcome once. Idempotent confirmation alone prevents a double-sell; only an idempotent charge prevents a double-charge. A crash can also outlast the hold's expiry. The retried confirmation still runs the conditional write, which succeeds if the seat is still available; if the seat sold to someone else in the meantime, the charge is refunded. What to watch: a seat marked sold with no successful payment behind it, or a successful charge with no seat — reconciling orders against payments and against seat status catches either mismatch directly.

What separates answers — the purchase-to-payment seam

BadCharge first, mark sold, no release path▾

GoodHold during checkout, convert on success, release on failure▾

GreatReserve-charge-confirm saga, idempotent confirmation, reconciliation▾

Key idea. The in-memory hold gives one fast winner per seat under a race, and the conditional write at purchase is the final guard if a hold is lost; the waiting room protects the service from the crowd that creates that race, without promising a seat; and treating purchase as a small saga keeps the hold, the charge, and the order consistent across a payment failure or a crash.

## 7. Variants

### 10× scale

More events and bigger on-sales shard the hold store and the Seat DB further by event, but a single hot seat is irreducible — its one hold key and its one conditional write must stay cheap regardless of how much else scales around it. The waiting room scales horizontally and its admission rate adapts to inventory-service latency; the browse cache absorbs nearly all of the read growth, since availability reads dwarf hold attempts by a wide margin. At this scale, failovers of hold-store shards happen more often, so the zero-row purchase rate, and the refunds it causes, becomes a metric to track.

### General admission (no assigned seats)

Inventory becomes a single counter per tier, so a hold is an atomic decrement (remaining > 0 ? remaining-- : reject) rather than a per-seat set-if-absent. Each hold still needs its own expiring record, so an abandoned hold can add its unit back to the counter. One counter per tier is itself a hot key — every buyer now hits it — but fungible inventory can be distributed: sharded counters or pre-allocated blocks spread the load while keeping the same final guard at purchase and the same waiting room. The problem gets easier because inventory is interchangeable, not because contention disappears.

### Resale / transfer

Reselling a ticket is a change of ownership on an already-sold seat, paired with a new payment between two users — the inventory count never changes, so it's a wallet-style transfer layered on an existing order, not a new hold against inventory.

Key idea. The architecture holds at 10× scale because a hot seat's cost is irreducible regardless of sharding elsewhere; general admission replaces per-seat contention with a counter; and resale is an ownership transfer on existing inventory, not a new hold.

## 8. The transferable pattern

Selling limited inventory under a stampede is an expiring claim in a fast store, a final conditional write in the database of record, and a waiting room. The claim absorbs the contention and gives each buyer a fast answer. The conditional write enforces correctness once per sale. The waiting room turns a wall of simultaneous demand into a manageable stream. The same design reappears anywhere fixed, contended inventory meets a demand spike that dwarfs it — flash sales, limited-release product drops, and any other "the first N people get it" system.

## Review: the 30-second answer

- Hold, then purchase — grabbing a seat creates a short-lived hold so no one else can take it while checkout completes, and the hold expires if the buyer doesn't finish in time.

- The hold is a set-if-absent with an expiry in an in-memory store (for example SET ... NX EX 600): the first request wins, the others get 409, and expiry needs no sweeper.

- No overselling: after payment, one conditional write in the strongly consistent database (UPDATE ... WHERE status = 'available') marks the seat sold. If a lost hold lets two buyers pay, only one write succeeds and the other buyer is refunded.

- A waiting room in front of the buying flow admits users at a controlled, roughly-fair rate and issues an admission token that the booking API checks on hold — it protects the service, it doesn't reserve a seat.

- Browse is cached and eventually consistent. Purchase hands off to the payment system as a small saga, releasing the hold on failure so the seat is not left stuck.

## Quiz

Ticketmaster Design Quiz

Hide AllReveal All

1)Why does a naive 'mark the seat sold on click' design fail even without considering scale?

2)A thousand requests try to hold the same seat in the same millisecond. Why does a set-if-absent produce one winner, when a read-then-write approach does not?

3)The in-memory store loses a hold key during a failover, and two buyers pay for the same seat. What happens, and why is the hold not enough on its own?

4)What does keeping the hold in the database (an available → held update with an expires_at column) gain and lose, compared with an in-memory hold?

5)Why doesn't sharding inventory by event help with contention on a single hot seat?

6)Why is a user being admitted from the waiting room not a guarantee that a seat is still available, and why does the booking API check an admission token?

7)Why does converting a hold to a sale need to be idempotent, given that a hold has already reserved the seat for one buyer?

## Sources and further reading

- SET command — Redis docs — the NX and EX options; SET ... NX EX creates a key with an expiry in one atomic command, the primitive behind the in-memory hold.

- Distributed locks with Redis — Redis docs — the SET NX plus TTL primitive behind a time-bounded claim, and the correctness caveats of lock expiry and failover that motivate the final conditional write.

- Cloudflare Waiting Room — Cloudflare — surplus users wait on a waiting page so origin servers are not flooded.

- How Queue-it works — Queue-it — overflow visitors are redirected with an HTTP 302 to a waiting room and sent back to the site in order.

- Virtual Waiting Room on AWS — AWS Solutions — tokens admit users in controlled waves, with queue state kept in an in-memory cache and a database.
