---
layout: simple
title: "System Design Primer — System Design School"
permalink: /system_design/sds/concepts/primer
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

System Design Primer12

★The TemplateIntroductionWhat Is System Design?What Are System Design Interviews?Level Expectations

Show all 12 →

Design Solutions35

LeetCode (Online Judge)Typeahead / AutocompleteDistributed Rate LimiterTicketmasterNews Feed

Show all 35 →

AI System Design6

RAG SystemChatGPTImage Generation ServiceCoding Agent CLI (Claude Code)

Show all 6 →

Patterns5

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time Transport

Show all 5 →

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# System Design Primer

## Introduction

Companies test system design in interviews, especially for senior roles. The skill also matters outside interviews. Most engineering roles expect engineers to write code, but a system that must scale and stay reliable needs broader knowledge of how its components work together.

The quickest way to prepare

If you already know what a system design interview is about and want the quickest way to prepare, go to the template. Many interview questions share one design: writes go into a queue, workers update the database and the cache, and reads come from the cache. The template page builds it one box at a time and works through example interview questions with it. For the time it takes, it gives the most return of anything in your prep.

Read the full article →

## What Is System Design?

System design is the process of defining the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements. The result is a blueprint for a complex software system that is efficient, reliable, and scalable.

In practice, system design means making technical trade-offs that turn a vague problem into a scalable solution. Each connection in the diagram should trace back to one of the system's constraints, such as the expected traffic, the amount of data, or the response-time target.

### System Design vs Object-Oriented Design

System design interviews differ from object-oriented design interviews in several ways, as the table shows.

AspectObject-Oriented DesignSystem Design

Example ProblemsDesign a parking lot, elevator controller, chess game, vending machineDesign Twitter, YouTube, Uber, Netflix

ScaleSingle machineLarge scale, millions of users, petabytes of data, multiple data centers

FocusCode structure, class relationships, design patternsArchitecture, distributed systems, scalability

Skills TestedClass design, inheritance, interfaces, SOLID principlesComponent selection, data flow, partitioning, replication, trade-offs

OutputUML diagrams, code implementation, class hierarchiesArchitecture diagrams, capacity estimates, API design, database schemas

ExecutionCode runs on single processServices span multiple servers and regions

Some skills carry over from one interview type to the other. An object-oriented design answer is judged mostly on clean code and maintainability. In a system design answer, the code matters less than how the system holds up at scale, which brings performance, reliability, and cost to the front of the discussion.

## What Are System Design Interviews?

Writing code becomes less central as careers progress. Companies need engineers who design systems for high traffic, balance cost against performance, and lead technical discussions. System design interviews assess these capabilities.

These interviews start at mid-level roles and become central for senior positions. At senior levels, engineers contribute to application architecture and make design choices that affect entire systems. The interviews simulate real-world scenarios that involve scalability, fault tolerance, and performance.

A production system can take a team months or years to build, and a system design interview usually lasts under an hour.

### What System Design Interviews Test

The interview checks whether a candidate can break down a vague, open-ended problem into solvable parts. It also checks how well the candidate understands component interactions and designs scalable, reliable, maintainable systems.

Every design decision has trade-offs, so explain why you chose one approach over another. Communication matters as much as technical depth. In real work, engineers explain designs to teams and stakeholders, and clear explanations make that collaboration possible. A design rarely follows a straight path. Adjust your approach when new constraints or feedback appear.

## Level Expectations

Interview expectations change with seniority. When you know what your level requires, you can focus preparation on the right topics.

The main difference between levels is how much ambiguity a candidate must handle. Junior engineers receive well-defined problems with clear requirements. At the senior level, problems are deliberately vague, and the candidate must clarify and decompose them. Staff engineers face the most ambiguity and often define the problem space themselves.

Problem complexity follows the same pattern. L4 problems have simple contracts: given input A, return output B. L5 problems combine 2-3 concepts with some flexibility. L6 problems either combine 4-5 subsystems or present abstract requirements that need significant clarification before design begins.

Expectations also differ by company. The widget has two views: one gives the scope, the depth, and an example deep dive for each level, and the other compares how companies name and pace their levels.

By levelBy company

L4 · MidL5 · SeniorL6 · Staff

Problem scope

Well-defined problems with guidance

Depth expected

Surface-level understanding

Common topics

Cache, database, load balancer, API design

Interview focus

Template execution, component knowledge, basic trade-offs

L4 problems have simple contracts. TinyURL takes a long URL and returns a short one. A YouTube view counter takes a video ID and returns a count. These are solved problems with standard solutions.

The interview is mechanical: clarify requirements, design APIs, draw the architecture, then a light deep dive. Since the solution is known, interviewers have low tolerance for messy structure. You must own the template.

You need the basic building blocks — load balancer, cache, database, message queue — plus when to use SQL versus NoSQL and vertical versus horizontal scaling. Deep dives stay surface-level: "LRU removes least recently used items" is enough.

Most candidates fail from poor time management, not from lacking knowledge. They run out of time or present a disorganized design.

Depth ladder — “strong consistency”: What is strong consistency? — concept awareness

Problem scope

Clearer requirements, some ambiguity

Depth expected

Moderate depth on 1–2 components

Common topics

Scaling patterns, partitioning, caching strategies, message queues

Interview focus

Architecture choices, trade-offs, common scale challenges

L5 problems scale a specific feature. Top-K songs combines counting and ranking. Flash sales need distributed counters with consistency. News feed sits on the L5/L6 boundary — at L5 you focus on fan-out (push versus pull) and basic storage.

The interview has moderate ambiguity. You must ask about scale and constraints proactively. The mental shift is from "How do I build a component?" to "How do I scale this feature without breaking?" You should identify bottlenecks without prompting.

You need to know how scaling patterns actually work. "Hash-based partitioning on user_id ensures even distribution" — then the trade-off when pushed: "it avoids hotspots, but resizing the cluster is painful."

Deep dives go deeper. Spend real time explaining 1–2 components in detail. The challenge is balancing breadth (the full design) with depth (the hardest bottlenecks).

Depth ladder — “strong consistency”: How do we implement strong consistency? — implementation knowledge

Problem scope

Ambiguous requirements, must clarify scope

Depth expected

Deep dive on 2–3 components

Common topics

Distributed systems, consistency, replication, consensus, failure handling

Interview focus

Navigating ambiguity, deep knowledge, production reality

L6 problems are either highly ambiguous or infrastructure-level. Design a distributed job scheduler. Design an ad-serving system. These are not features — they are the platform other engineers build on, and they demand strict guarantees: exactly-once, ordered processing, no data loss.

The interview has no template. You lead. Aggressively manage time: "Standard load balancer and SQL for user auth, let's move on." Buy time for the novel problem. Identify what is actually hard: "The hard part isn't storage. It's preventing two workers from grabbing the same job when the network is slow."

You must understand guarantees and failure modes deeply — practical reality, not textbook definitions. "A worker crashed after processing a payment but before sending the success signal. The scheduler retries. Now you charged the user twice. Fencing tokens? Database constraints? Leases?"

The interviewer probes every decision and ties it to business impact: "Why strong consistency over eventual?" and "What if requirements change to prioritize availability?" Your job is defending trade-offs under changing constraints.

Depth ladder — “strong consistency”: Why this implementation, and why strong versus eventual here? — trade-off justification

GoogleMetaAmazonMicrosoftApple

Entry

L3

Mid

L4

Senior

L5

Staff+

L6–L8

Google. Slow progression, high bar for senior+. L5 is terminal for most. Expect 3–5 years between levels.

Entry

E3

Mid

E4

Senior

E5

Staff+

E6–E9

Meta. Faster progression than Google. E5 achievable in 2–3 years. Performance-driven culture.

Entry

SDE I

Mid

SDE II

Senior

SDE III

Staff+

Principal+

Amazon. Faster initial progression. Strong leadership-principles emphasis. L6+ requires scope beyond code.

Entry

59–60

Mid

61–62

Senior

63–64

Staff+

65+

Microsoft. Slower progression. System design starts at 62+. Emphasis on cross-team collaboration.

Entry

ICT2

Mid

ICT3

Senior

ICT4

Staff+

ICT5+

Apple. Secretive leveling. Very slow progression. Product-focused, less emphasis on pure scale.

Titles at junior and mid-levels are roughly equivalent across companies, but diverge sharply at senior levels. Google favors slow, tenure-heavy progression while Meta rewards rapid impact. Amazon has the "SDE II trap," where reaching Senior needs cross-team scope equivalent to Staff elsewhere. Microsoft climbs steadily until the "Principal cliff" at 65. Apple is design-driven and rigid — you wait to be assigned larger projects rather than creating scope.

## How to Prepare

### Why Memorized Solutions Fall Short

A common approach is to collect popular system design problems, watch videos of their solutions, read blog posts with architecture diagrams, and memorize the answers.

Say a video explains how to design Twitter with microservices, message queues, a cache, and a wide-column database, and you memorize that diagram. If the interview asks for Twitter, you can draw it. If you studied 30 solutions and the question is a system you have not seen, you try to bend the Twitter design to requirements it was not built for, without knowing why each part was in it.

The same gap shows up on a familiar problem. Solutions to the common problems are public and widely studied, so the follow-ups ask why a component is there and what it costs. At L5 a memorized diagram gets you through the first part of the discussion. At L6+ most of the interview is deep dives into one or two components, which a memorized diagram does not cover.

### How to Study Instead

Learn how each component works and why a design uses it. With limited time, start with the common patterns and the templates, then practice them on 10-15 common problems. For each problem, go past the solution: work out what breaks if you remove the cache, or what changes if a relational database replaces the wide-column one.

### What the Primer and the Course Cover

System Design School teaches the fundamentals first, starting from the building blocks that designs are made from.

This primer is a short overview of the main components, the interview templates, and the mental models for common problems.

The full course has two tracks:

Fundamentals covers the core building blocks that appear in most system design interviews:

- Microservices & Communication: message queues, Kafka, circuit breakers, service discovery.

- Scaling Services: load balancing, auto-scaling, caching patterns such as cache-aside and write-through, CDNs, and the thundering herd problem.

- Data Storage: B-trees, LSM trees, SQL versus NoSQL, document versus key-value stores, OLTP versus OLAP.

- Scaling Data: replication (primary-replica, multi-leader), partitioning (consistent hashing, range-based), change data capture, rebalancing.

- Batch & Stream Processing: MapReduce, stream processing, and the lambda architecture.

- Patterns: rate limiting, unique ID generation, sagas, fan-out and fan-in.

Domain Knowledge covers specialized topics that appear in specific problem types:

- Transactions: isolation levels, pessimistic and optimistic locking, flash-sale inventory.

- Distributed Systems: the CAP and PACELC theorems, consistency models, consensus (Raft, Paxos), failure handling.

- Geospatial Search: geohash, quadtrees, H3 hexagons, the S2 library.

- Search Engines: inverted indexes, TF-IDF and BM25 ranking, Elasticsearch architecture.

- Media Systems: video transcoding, file chunking, adaptive bitrate streaming.

- Probabilistic Data Structures: Bloom filters, count-min sketch, HyperLogLog.

The full course covers single topics in more depth.

### Where to Start

Pick a starting point by how much time you have:

- Interview tomorrow: The System Design Template, the pattern that fits most common problems, with worked examples.

- A few days: Core Design Challenges and Designing for Scale.

- New to system design: the main components.

- You know the components and need an interview structure: the step-by-step walkthrough.

### How This Primer Is Organized

It starts with what breaks when one machine is not enough (Core Design Challenges, Designing for Scale) and how to stay correct once data is copied across machines (Consistency and Tradeoffs). The Master Template and Main Components then combine those techniques into one design that fits most questions. The last two sections, the decomposition framework and the step-by-step walkthrough, are about getting from a short prompt to that design inside an interview.

## Core Design Challenges

Once traffic or data outgrows one machine, most system design problems run into some of the same four challenges.

### Challenge 1: Too Many Concurrent Users

A large user base introduces many problems. The most common one is that a single machine or database has an RPS/QPS limit. The single-server demo apps in web development tutorials slow down fast once traffic passes that limit.

Replication removes this limit. Run copies of the same asset and assign users at random to each copy. When the copied asset is server logic, this is called load balancing. When the copied asset is data, the copies are called database replicas.

### Challenge 2: Too Much Data to Move Around

The companion problem to too many users is too much data. Data becomes big when one machine can no longer hold all of it. Examples include a web search index, every post on a large social network, and the full library of a video streaming service.

Sharding spreads that data across machines by partitioning it on a chosen key, and the sharding logic decides which records sit together. If Twitter shards by user_id, all tweets from one user live on the same machine.

### Challenge 3: The System Should be Fast and Responsive

User-facing apps must respond quickly. Usability research puts the limit for keeping a user's flow of thought at about 1 second (Nielsen Norman Group), and many teams set a lower target, such as 500ms.

Reads are usually fast once replication is in place. Most read requests become lookups in an in-memory key-value store behind an HTTP endpoint. For many small apps, network round-trip time accounts for most of the latency.

Writes are the harder part. A typical write runs many queries and updates, so it can take much longer than a single read. With asynchrony, the user does not wait for that work. The server receives the data, puts it in a queue, and returns a response at once. The backend then does the actual processing.

This gap gives client-side logic room to keep the experience fast. For example, the client can show a confirmation screen before it redirects the user to read the result. That step gives the backend time to finish the write.

Message queues such as Kafka implement this pattern.

### Challenge 4: Inconsistent (outdated) States

This challenge comes from the solutions to Challenge 1 and Challenge 2. With replicated data and asynchronous updates, a read request can see inconsistent data. Here, inconsistent usually means outdated. Users do not see random wrong values, but they can see old versions or data that was already deleted.

Most of the fix happens in the application, with less of it in the infrastructure. Outdated reads from replication and asynchronous updates go away once the servers catch up. Design the user experience so that a short window of outdated data is acceptable. This model is called eventual consistency.

Most apps tolerate eventual consistency well, because the alternatives are lost data or slow responses. Banking and payment apps are the exception. Showing a wrong balance is not acceptable there, so the app waits for all processing to finish before it returns a response, and these apps respond more slowly as a result.

## Designing for Scale

Scaling is a large part of meeting non-functional requirements, and scalability is often the top priority. The strategies below each address a different source of load.

### Estimating the Load

Estimate the load before you choose a strategy. Estimation shows which quantity drives the design: reads, writes, storage, or peak burst. Derive each number from usage instead of asserting it, as the calculator does from a few usage assumptions.

Daily active users500K

Write actions / user / day1

Reads per write5:1

Peak-to-average factor3×

Stored bytes / write50 KB

Retention10 yr

Writes / sec (avg)

5.8

Reads / sec (avg)

28.9

Reads / sec (peak)

86.8

Storage after 10 yr

91.3 TB

writes/s = 500K × 1 ÷ 86,400 = 5.8/s
reads/s (peak) = 5.8 × 5 × 3 = 86.8/s

Round aggressively — these are order-of-magnitude numbers. The point is to find which quantity is large enough to drive the design.

The calculation follows the same steps in most cases. Daily actions divided by 86,400 seconds gives an average rate. Multiply that rate by a peak factor for the burst the system must handle. Reads usually outnumber writes by a large margin, so caching and replicas go on the read path. See Back-of-the-Envelope Estimation.

### Decomposition

Decomposition breaks requirements down into microservices. Each service is small and independent, and it maps to a specific business capability or requirement. A service with a single responsibility is easier to scale and maintain.

### Vertical Scaling

Vertical scaling is the brute-force approach: scale up by moving to a more powerful machine. Cloud computing made this approach much more practical. In the past, organizations waited for new machines to be built and shipped. Today they start new instances in seconds.

Cloud providers offer very large machines for vertical scaling, with terabytes of memory and many CPU cores, at a much higher price than small ones.

### Horizontal Scaling

Horizontal scaling scales out by running multiple identical instances of a stateless service. Because the instances hold no state, a load balancer can send any request to any instance.

### Partitioning

Partitioning splits requests and data into shards and spreads the shards across services or databases. The partition key can be the user ID, the geographic location, or another logical key. Many systems use consistent hashing to keep the partitions balanced.

Plain hash-mod-N partitioning has one large problem. When the shard count changes, almost every key moves to a different shard. Consistent hashing fixes this. It places both nodes and keys on a ring, and each key belongs to the next node clockwise. When a node joins or leaves, only the keys in one arc move, which is about 1/N of them. In the widget, watch which keys change owner when a node joins the ring.

Basic (1 point / server)Virtual nodes (3 / server)

+ Add Server D✕ Fail Server C↺ Reset

Keys remapped by last change (gold ring = moved key)

—

Keys owned per physical server:

Server A

4

Server B

5

Server C

3

Colored arcs show which server owns each slice of the ring. Click Fail Server C or Add Server D to watch only the neighboring arc remap.

See Database Partitioning and
Consistent Hashing for details.

### Caching

Caching improves read performance by keeping frequently accessed data in faster storage, such as an in-memory cache. Tools such as Redis and Memcached hold hot data and reduce database load.

The hit rate decides how much load the cache removes. Origin load equals total load times the miss rate, so the last few percent have the largest effect. An increase from 90% to 99% cuts database traffic by another 10×, because the miss rate falls from 10% to 1%.

Cache hit rate90%

Total read QPS50.0K

▶ Play streamReset

Press play — each square is a read. Green = cache hit, red = origin miss.

Reaches the database

5.0K/s

Effective read capacity

10.0×

A 90% hit rate sends only 5.0K/s to the database instead of 50.0K/s. The last 10% of hit rate matters most: going 90% → 99% cuts origin load by another 10×.

See Caching for details.

### Buffer with Message Queues

Write-intensive operations are common under high concurrency. Frequent database writes can overload a system because disk I/O becomes the bottleneck. A message queue buffers write requests and makes the writes asynchronous. The database then receives writes at a rate it can handle, and a burst does not crash the system.

The widget has two modes. In Direct to server mode, traffic above the server's capacity overloads the single server, and it starts to drop requests. In Buffer with a queue mode, the same burst goes into the queue and drains at the server's steady rate, so requests wait longer but none are dropped. If the overload continues long enough, it fills the buffer too.

Base traffic80 req/s

Server capacity100 req/s

Direct to serverBuffer with a queue

▶ PlayBurst +150 req/sResetA mode change clears the counters.

Producer

80 req/s

Server

100/s

Processed

0

Dropped

0

Dropping now

0/s

Traffic is 80 req/s, and the capacity is 100 req/s. Press Burst to send 3 seconds of extra traffic.

The queue holds up to 500 requests, and a burst lasts 3 seconds. Both numbers are illustrative. The queue card shows the depth and the estimated wait.

See Message Queues for details.

### Separating Read and Write

Whether a system is read-heavy or write-heavy depends on the business requirements. Social media platforms are read-heavy, since users read far more posts than they write. In an IoT system, devices send readings continuously, so writes outnumber reads. Separate read and write operations so that each path can be handled differently.

Read and write separation usually uses one of two strategies. The first is replication with a leader-follower architecture. Writes go to the leader, and the followers serve as read replicas.

The second is the CQRS (Command Query Responsibility Segregation) pattern. CQRS goes further and uses separate models for reading and writing data. It splits the system into two parts. The command side (write side) handles all write operations (create, update, delete) with data models optimized for writes. The query side (read side) handles all read operations with denormalized data models optimized for reads.

Changes from the command side propagate to the query side asynchronously.

For example, a system can use MySQL as the source-of-truth database and Elasticsearch for full-text search or analytical queries. MySQL binlog Change Data Capture (CDC) syncs the changes from MySQL to Elasticsearch asynchronously.

### Combining Techniques

Scaling usually requires several techniques together. Start with decomposition, which breaks a monolith into services that scale independently. Partitioning and caching then work together to spread load and improve performance. Read/write separation with leader-replica setups gives fast reads and reliable writes. Finally, changes to business logic can remove operational bottlenecks without a worse user experience.

In the combined architecture below, a load balancer spreads client traffic across two services. Service A reads from a cache and sends its writes to a queue, from which a worker writes them into a sharded primary database. A replica of the first shard takes some of the reads off its primary.

### Adapting to Changing Business Requirements

A change to the business requirements is another way to handle large traffic loads. These strategies are not strictly technical, but they are practical answers to a load problem.

Consider a weekly sales event. Instead of running all sales at the same time for all users, spread the load. Assign specific days to different product categories in specific regions. For example, baby products are on sale on Day 1, and electronics are on sale on Day 2. Traffic becomes more predictable, and resources can be planned ahead. The system can pre-load the cache for upcoming days and scale out read replicas in specific regions.

Consistency during an online auction is another example. The frontend shows a temporary bid success message, and the backend resolves consistency issues asynchronously. The user experience stays smooth, and users eventually see the correct bid status after the auction ends.

## Consistency and Tradeoffs

Replication and asynchronous updates let a system handle more load. They also let
readers see stale or conflicting data, which is the problem Challenge 4 described.
Each feature needs a decision about how fresh its reads must be, and features can make
different choices.

### The CAP Theorem

CAP says a distributed store can hold only two of three properties at once:
Consistency (every read sees the latest write), Availability (every request
gets a response), and Partition tolerance (it keeps working when the network
drops messages between nodes). In the diagram, the three properties are overlapping
circles, and each pairwise overlap is a combination that a system can have, with
example databases listed inside it.

Highlight CAHighlight CPHighlight AP

CPHBase · MongoDB · Redis — stays consistent, refuses on the cut-off side

APCassandra · DynamoDB · Riak — stays available, may serve stale data

CAsingle-node SQL — only possible without partitions

The center — all three at once — is not achievable. Across machines partitions happen, so P is a given, which leaves the real choice as CP versus AP.

In a system that spans machines, partitions will happen, so P is not optional.
That reduces the real choice to two edges. CP keeps data correct by refusing
requests on the cut-off side. AP stays up by serving possibly stale data.
The CA corner exists only for a single node that never partitions.

The next widget runs a leader and a replica that copies its writes after a
set lag. When Simulate partition cuts the replica off, the AP setting keeps
answering reads with stale data. Under CP, the replica refuses to answer while
it is cut off.

AP · read replica, allow staleCP · require leader

▶ Play writesSimulate partitionReset

Replica lag2 versions

Leader (source of truth)

v0

Replica

v0

A read now returns v0 — fresh.

Turn on the partition: AP keeps answering with stale data, CP stops answering. That is the choice CAP forces once the network splits.

Most consumer features choose AP, since a social feed that is a few seconds out of
date still serves its reader. A payment feature cannot show a wrong balance, so it
chooses CP and accepts that some requests wait or fail during a partition. See
CAP and PACELC Theorem.

### Consistency Models

Consistency has several levels between strong and weak. Strong consistency means
every read sees the latest write. Eventual consistency means replicas converge
over time, so reads may lag. Read-your-writes sits between the two: a user sees
their own updates at once, even if other users see them later.

These levels differ only in what a read may return in the moments after a write,
while replicas are still catching up. In the widget, a new value is committed, and
two readers watch the replica sync: the author who wrote the value, and another user.

StrongRead-your-writesEventual

▶ PlayResetauthor writes v2 at t=0 · replica lag 3 ticks

replica synced

You (the author) reads

v2

fresh

Another user reads

v2

fresh

Strong. Every read sees the latest write. Reads go to the leader or wait for replicas, so no one ever sees stale data.

Stronger levels send reads to the leader or wait for replicas to confirm, which
adds latency and lowers availability. Weaker levels read whichever replica is closest
and may return stale data. Many systems let you tune the level per read and per
write, so each feature can use the weakest level at which stale reads do it no harm.
See Data Consistency Models.

### Contention and Concurrency

When two clients update the same record at once, a naive read-modify-write loses
one update. Both clients read the old value, and the second write overwrites the
first. The widget plays this race, and then the same two writes under an optimistic
lock.

Naive read-modify-writeOptimistic lock (version)

◀▶Play

two clients both increment the same counter

Stored count

10

T1read count → 10

Optimistic locking adds a version column and writes with UPDATE … WHERE version = N. If another writer already bumped the version, the update matches zero
rows; the losing writer re-reads and retries. This method assumes conflicts are
rare, so it adds cost only when a conflict occurs. Pessimistic locking takes a
lock up front instead and trades throughput for certainty. See
Database Transactions.

### Multi-Step Workflows and Sagas

A checkout spans several services: reserve inventory, charge payment, create a
shipment. No single transaction covers all of them. A saga runs the steps in
order. If one step fails, the saga runs compensating actions to undo the earlier ones.

The failure point in the widget can be any step. The steps commit in order, and when
one fails, each step that already committed is undone in reverse order by its
compensation.

Fail at:Reserve inventoryCharge paymentCreate shipmentNone

Reserve inventory

waiting

→

Charge payment

waiting

→

Create shipment

waiting

◀▶▶ Play1 / 5

Saga starts. Each step runs in order.

Suppose the payment step charges a card and the shipment step then fails. The charge
has already committed, so the saga cannot erase it the way a database rollback would.
It issues a refund instead, a new action that reverses the completed step. Releasing
an inventory hold works the same way. Each step and each compensation must be
idempotent, because retries can repeat them. See
Saga Pattern.

## Master Template

This template is a common starting design for scalable services and for many system design problems.

In summary: write to a message queue, and let consumers (workers) update the database and the cache. Serve reads from the cache.

The template, worked through example questions

See which part of the template carries LeetCode, YouTube, a URL shortener, post search, and a chat app, and where Ticketmaster and a news feed add one more piece.

Read the full article →

The template is easier to justify when it is built one box at a time. In the builder,
each step names the problem that forces the next component. The same order works for
presenting the components in an interview.

◀ BackNext ▶▶ PlayStep 1 / 8

Client

Client

→

App server

Service

→

Database

Storage

One server, one database

Start with the smallest thing that works: a client calls one app server, which reads and writes one database.

Reveal one box at a time. In an interview, add each component only when a concrete problem forces it — never all at once.

The next diagram shows the composed core. Clients reach stateless app servers through
a load balancer. Reads come from a cache backed by a primary-replica database. Slow
writes flow through a queue to background workers.

### Component Breakdown

Stateless Services scale out: you add new machines and put them behind load balancers. The Write Service receives client requests and forwards them to message queues. The Read Service handles read requests from clients by reading from caches.

Databases are the cold storage and the source of truth. Reads do not normally go directly to the database, because it becomes slow when request volume is high.

Message Queues sit as a buffer between the write services and data storage. Producers (the write services) send data changes to queues, and consumers update both databases and caches. Two asynchronous workers do the consuming: the Database Updater takes jobs from the queues and updates databases, and the Cache Updater takes jobs from the queues and refreshes caches.

Caches make read operations fast.

### Dataflow Path

Most applications break down into read requests and write requests. A read does not change data, and a write changes the database. Because the two have different effects, we discuss the write path and the read path separately.

Read path: Modern large-scale applications with millions of daily users usually read from the cache instead of from the database directly. Databases act as permanent storage, and asynchronous jobs often copy data from databases to caches.

Write path: Write requests go into message queues, and backend workers handle the writes. The queue absorbs differences in processing speed between components, so the user gets a fast response.

The write path accepts the request, enqueues it, and returns immediately. A worker
then persists the data to the database and updates the cache asynchronously.

The read path answers from the cache and reads the database only on a miss.

Message queues let a system scale out to handle write requests. Producers insert messages into queues, and consumers retrieve and process them asynchronously.

A system needs message queues for two reasons. Producers and consumers process data at different speeds, so they need a buffer between them. Queues also persist messages, which prevents data loss when a component fails.

## Main Components

Many common system design problems already have known solutions, which engineers packaged as reusable building blocks called components. Most systems use several of them, and a system design answer is mostly an assembly of these components. For that reason, it helps to know how each technology works and when it fits.

### Microservices

#### The Problem

Consider an e-commerce application where everything lives in one codebase: product catalog, checkout, payments, and user accounts. At 100 orders per day, this monolithic approach (one application that deploys as a single unit) works.

Two years later, traffic grows to 10,000 orders per day. Checkout needs more servers, but the team cannot scale checkout alone, so it must scale the entire monolith. The payment team wants to deploy fraud detection, and each deploy requires coordination with every other team. A bug in the catalog crashes the whole application and takes down checkout and payments with it.

The microservices approach splits the application into independent services, each handling one business function. The e-commerce system becomes a Product Service, Cart Service, User Service, Order Service, and Payment Service. Each service can deploy, scale, and fail without affecting the others.

#### How Microservices Work

Each service runs as a separate process. Services communicate through APIs, typically REST over HTTP or gRPC. The Payment Service calls the Order Service to verify order details, and the Order Service calls the Inventory Service to check stock. No service talks directly to another service's database.

Each service owns its database. The User Service manages the User Database, and the Order Service manages the Order Database. Because no other service reads those tables, the User Service can change its database schema and the other services keep working.

Services register with a service registry (like Consul or Eureka). When the Payment Service starts, it announces its location to the registry. Another service that needs to call the Payment Service asks the registry where to find it. This lookup is called service discovery.

Services scale independently because they have different load patterns. During a holiday sale, checkout traffic spikes. The team adds 10 more Order Service instances, while the Product Service keeps running on 2 instances.

Fault isolation limits cascading failures. If the Recommendation Service crashes, checkout still works. Services use circuit breakers to detect failures and stop sending requests to broken services.

For more on microservices architecture, communication patterns, and service mesh, see Microservices and Monolithic Architecture.

#### Common Implementations

Spring Boot is a Java framework for building microservices. It includes built-in support for REST APIs, service discovery, and distributed tracing, which suits enterprise systems that need mature tooling and strong typing.

Teams that prefer JavaScript or TypeScript often build lightweight microservices with Node.js and Express. Development is fast, and the npm ecosystem is large.

Go, with frameworks like Gin or Echo, has concurrency built into the language through goroutines. Teams use it for high-throughput services, like real-time bidding or stream processing.

### Relational Databases

#### The Problem

Money transfers show why some data needs strict rules. When User A sends $100 to User B, the system must subtract $100 from A's account and add $100 to B's account. Both operations must succeed or both must fail. If only the first step completes, User A loses $100 and User B never receives it.

This requires consistency: data must remain accurate across related records. Relational databases provide it through structured storage and ACID transactions.

Relational databases organize data into tables. Each table has rows and columns. A Users table has columns for user_id, name, and email, and each row represents one user. Tables link through relationships, so an Orders table references Users through a user_id column.

Use a relational database when consistency is critical. Financial transactions, inventory management, and user account systems require accurate, structured data. NoSQL databases give up some of these guarantees in exchange for schema flexibility.

#### How Relational Databases Work

Tables store structured data, and each table represents an entity: Users, Orders, Products. Columns define the schema, which sets data types and constraints. Rows contain the records.

Primary keys uniquely identify each row. The Users table has user_id as its primary key, so no two users share the same user_id. Foreign keys create relationships between tables. The Orders table has a user_id column that references the Users table, which links each order to a specific user.

Three relationship types exist:

- One-to-one: each user has exactly one profile

- One-to-many: one user has many orders

- Many-to-many: many students enroll in many classes, requiring a junction table storing both student_id and class_id

The ACID properties describe how a transaction keeps data correct:

- Atomic: transactions complete fully or not at all

- Consistent: transactions move the database from one valid state to another

- Isolated: concurrent transactions don't interfere

- Durable: committed transactions persist even after crashes

Because a SQL query can join tables to combine data, filter rows with WHERE clauses, and aggregate with GROUP BY, relational databases are a good fit for complex business logic.

For more on relational databases, indexing strategies, and query optimization, see Relational Database Fundamentals and Database Partitioning.

#### Common Implementations

PostgreSQL is an open-source relational database with advanced data types (JSON, arrays), full-text search, and custom functions. These features help applications that run complex queries or analytical workloads alongside transactional operations.

MySQL is an open-source relational database with good read performance and straightforward replication. Web applications that prioritize simplicity and broad hosting support often choose it.

Amazon RDS is a managed relational database service that supports PostgreSQL, MySQL, and others. It runs backups, patches, and scaling for the team.

### NoSQL Databases

#### The Problem

A photo-sharing app stores user posts. Each post has an image, caption, hashtags, location, timestamp, and comments, and each comment contains text, an author, and nested replies. Fitting this into relational tables requires many joins. The Posts table joins to Comments, which joins to Users, which joins to Locations. Reading one post requires queries across all of these tables, plus one for hashtags.

Suppose the schema also changes weekly. The product team adds "story reactions" one week and "polls" the next. Each schema change requires a database migration coordinated across teams, and development slows down.

A NoSQL document database stores this flexible, nested data without a rigid schema. One document holds everything: the post image, caption, comments array, and location object. A read needs no joins, and a schema change needs no migration.

NoSQL fits data whose structure varies by record or gains new fields often. It also fits very high write volumes spread across many servers. In return, it gives up relational guarantees for flexibility and horizontal scalability.

#### How NoSQL Databases Work

NoSQL databases come in four types, each optimized for different access patterns. The widget shows how each type stores a sample record.

Key-valueDocumentColumn-familyGraph

session:abc123→{ "user_id": 456, "exp": ... }

cart:u456→["sku_1", "sku_9"]

rate:ip:1.2.3.4→27

A giant hash map. O(1) lookup by key, no queries across values.

Best for: caching, sessionsExamples: Redis · DynamoDB

- Key-value stores work like hash maps, which makes them a common choice for caching and session management. A session can be stored with key session_abc123 mapping to JSON {"user_id": 456, "login_time": "..."}. Redis and Memcached are examples.

- Document databases store JSON-like documents. Each document is self-contained with nested fields. MongoDB is a document database, and content management, where records have varying schemas, is a typical use.

- Column-family stores organize data by column instead of row. Cassandra stores time-series data efficiently, and column-family stores in general suit high-write workloads like logs and analytics.

- Graph databases store nodes and edges. Neo4j stores relationships as primary data, on the same level as nodes. Use them for social networks and recommendation engines.

NoSQL databases give up ACID guarantees for availability and partition tolerance. Most offer eventual consistency: writes reach all nodes, usually within seconds. Strong consistency is optional but reduces availability.

The articles NoSQL Database Fundamentals and CAP and PACELC Theorem cover NoSQL databases and distributed database concepts in more depth.

#### Common Implementations

MongoDB is a document database with rich queries, including filters, aggregations, and text search. Product catalogs and user-generated content, where documents have varying schemas, are common uses.

Redis is an in-memory key-value store. Beyond plain values, it supports lists, sets, and sorted sets, so it often backs caching, real-time leaderboards, and rate limiting.

Apache Cassandra is a distributed column-family database with no single point of failure. It spreads writes across nodes, which suits high write volumes. Use it for time-series data, event logging, and high-write applications.

Amazon DynamoDB is a fully managed key-value and document database. It scales capacity automatically, which helps serverless applications and workloads with unpredictable traffic patterns.

### Object Storage

#### The Problem

Consider a video platform that stores 100 million video files, billions of thumbnails, and the profile pictures its users upload. These files range in size from kilobytes to gigabytes. A relational database stores them inefficiently, because it is optimized for structured queries, not large binary files.

A file system works on one server but does not scale past it. A single server holds limited storage. More servers require manual partitioning logic, and replication for durability becomes complex. To read a file, the client must know which server holds it.

Object storage treats each file as an object with a unique ID. A video is stored under the key videos/user123/vacation.mp4 and retrieved later with that key. The system handles distribution, replication, and scaling automatically.

Typical uses are static assets like images and videos, backups that need long-term retention, and data lakes that hold raw data for analytics. Object storage is a poor fit for files that change often and for operations that need low latency.

#### How Object Storage Works

Objects live in buckets. A bucket is a container that can hold millions of objects. Each object has three parts: a unique key (like photos/cat.jpg), binary data (the file itself), and metadata (size, content type, custom tags).

There are no folders. Keys look like file paths, but the storage is flat. The key images/2024/cat.jpg is a plain string, and no /images/ directory exists.

Clients interact through RESTful APIs. A PUT request uploads an object, a GET request downloads it, and a DELETE request removes it. The API hides the underlying distributed storage.

Object storage replicates data across multiple nodes and regions. When a file is uploaded, the system automatically copies it to 3+ servers, so the data stays intact if one server fails. This replication is the source of object storage's high durability.

Versioning keeps multiple versions of the same object. If report.pdf is overwritten, the old version remains accessible, which protects against accidental deletions. Lifecycle policies automatically move old objects to cheaper storage tiers after 90 days or delete them after one year.

Consistency models vary. S3 offers strong read-after-write consistency, so a client can read an object immediately after it uploads it. Eventual consistency is cheaper, but reads can briefly return stale data.

For more on object storage systems and blob storage patterns, see Object Storage and Blob Storage.

#### Common Implementations

Amazon S3 stores objects with built-in replication and integrates with other AWS services. It covers most object storage needs, especially in AWS environments.

Google Cloud Storage provides multi-regional storage with strong consistency. Its close integration with BigQuery makes it a fit for Google Cloud applications and for running analytics on stored data.

Azure Blob Storage is Microsoft's object storage, used mainly by Azure-based applications and in hybrid cloud scenarios. It offers hot, cool, and archive tiers for cost optimization.

### Cache

#### The Problem

Product pages on an e-commerce site follow a common read pattern. Each page load queries the database for product details, price, and inventory. The database handles 1,000 requests per second, and most of these requests fetch the same 100 popular products again and again.

Each database query takes roughly 50ms, so page loads are slow. Database CPU reaches 90%. More database servers would add cost, and most queries return the same data they returned minutes ago.

A cache stores frequently accessed data in fast memory and answers repeated requests from that memory instead of from the database. For these product pages, response time drops from roughly 50ms to 1ms, and most of the database load goes away.

Caching fits workloads where reads far outnumber writes and some staleness is acceptable. For example, a product price can be 5 minutes old.

#### How Caches Work

The application checks the cache before it queries the database. On a cache hit, the data exists in the cache and the application returns it immediately. On a cache miss, the application queries the database, stores the result in the cache, and returns it to the user.

In the widget, repeated keys are hits. New keys miss, load from the database, and
fill the cache; when the cache is full, the least recently used key is evicted.

Cache size3 slots

▶ Step▶ PlayReset

Request

—

Cache — most recently used on the left

Hits

0

Misses

0

Hit rate

0%

On a miss the app reads the database, then fills the cache. When the cache is full, the least recently used key is evicted. Repeated keys become hits.

This pattern is called cache-aside, because the application manages the cache explicitly. Two alternatives exist. Write-through updates the cache and the database at the same time. Write-behind updates the cache first, then syncs to the database asynchronously.

Cache memory is limited. Eviction policies decide what to remove when the cache is full:

- LRU (Least Recently Used): removes items not accessed recently

- LFU (Least Frequently Used): removes items accessed rarely

- TTL (Time To Live): removes items after expiration

Cache invalidation keeps cached data fresh. With a 5-minute TTL on product prices, each entry expires after 5 minutes, and the next request fetches fresh data. For critical updates, invalidate the entry explicitly when the data changes. When a product price changes, delete that product's cache entry immediately.

TTL length sets a trade-off between freshness and database load. A longer TTL sends fewer queries to the database but serves staler data, and a shorter TTL does the reverse.

For more on caching strategies, eviction policies, and cache patterns, see Caching Fundamentals.

#### Common Implementations

Redis is an in-memory cache. It supports data structures such as strings, lists, sets, and sorted sets. Teams use it for session storage, leaderboards, and general-purpose caching.

Memcached is a simpler in-memory cache built for basic key-value storage, without the Redis data structures, so it suits cases where caching needs are basic and simplicity matters most.

CDNs like Cloudflare act as distributed caches for static assets. They hold images, CSS, and JavaScript files at edge locations worldwide, so content reaches users faster.

### CDN (Content Delivery Network)

#### The Problem

Suppose a news website hosts its videos in a New York data center. When a user in Tokyo clicks play, the request travels 11,000 kilometers to New York and back. Network latency alone is roughly 200ms, and the video stutters.

The load problem appears when millions of users watch the same viral video. The origin server in New York handles 10,000 requests per second, bandwidth costs rise, and as the server falls behind, some requests time out.

A CDN places copies of static content on edge servers distributed around the world. Tokyo users then fetch the video from a Tokyo edge server, and latency drops to roughly 5ms. Because the edge servers absorb most of the traffic, the origin server handles far fewer requests.

CDNs suit static assets such as images, videos, CSS, and JavaScript files. They help most in high-traffic applications with users around the world.

#### How CDNs Work

The site owner uploads static files to the CDN provider. The CDN replicates them to hundreds of edge servers across continents, in major cities such as Los Angeles, London, Tokyo, and Sydney.

A user in London requests https://cdn.example.com/logo.png. DNS routes the request to the nearest edge server in London. On a cache hit, the edge server has the file and serves it directly (5ms). On a cache miss, the edge server fetches the file from the origin (200ms), caches it locally, then serves it. Later London users get cache hits.

The edge hit rate decides how much traffic reaches the origin. As the hit rate in the
widget rises, more requests stop at the edge and origin load falls.

Play RestartRequests start cold — every cache is empty.

edge · NAcached: 0

edge · EUcached: 0

edge · APACcached: 0

origin shield

origin storage

requests

0

origin reads

0

cache hit rate

0%

Each file stays cached for its TTL (Time To Live). A logo that rarely changes can have a 24-hour TTL. Frequently updated content might use a 5-minute TTL. After the TTL expires, the edge server fetches fresh content from the origin.

A CDN also improves availability, because traffic spreads across many edge servers instead of one origin.

For more on CDN architecture and content delivery, see Content Delivery Networks.

#### Common Implementations

Cloudflare offers a global CDN with built-in DDoS protection and a web application firewall. Setup needs little configuration, and free tiers are available. Small to mid-sized applications that put security and ease of use first often start with it.

AWS CloudFront integrates with AWS services like S3 and Lambda@Edge, and it supports custom cache behaviors and edge computing. Use it for AWS-based applications that need programmatic cache control.

Akamai runs a large global network of edge servers. It offers advanced features like image optimization and predictive prefetching, and its main users are large enterprises with complex global delivery needs.

### Message Queues

#### The Problem

Direct calls between services break down under a traffic spike. During a peak sales event, an e-commerce site receives 10,000 orders per minute. The Order Service creates each order and calls the Payment Service, which takes 2 seconds per order. Because the Order Service waits for each payment to finish before it accepts the next order, orders pile up and users see timeout errors.

Then the Payment Service crashes for 30 seconds. During that window, 5,000 orders arrive and all of them fail. With no retry mechanism, that revenue is lost.

With a message queue between the two services, the Order Service sends order messages to the queue and responds to users immediately. The Payment Service processes messages from the queue at its own pace. If the Payment Service crashes, messages wait in the queue until it recovers, so the orders are not lost.

#### How Message Queues Work

Producers publish messages to the queue. For example, the Order Service publishes an order message: {"order_id": 123, "user_id": 456, "total": 99.99}.

The queue stores messages durably. Messages persist on disk, so they survive a queue server crash. Each message waits until a consumer is ready.

Consumers pull messages from the queue and process them. The Payment Service pulls the order message and charges the user. After it processes the message, the consumer sends an acknowledgment to the queue, and the queue deletes the acknowledged message.

In the widget, a healthy consumer receives, acks, and removes each message. When the
consumer is set to failing, unacked messages are redelivered, and after several attempts
they move to a dead letter queue instead of blocking the line.

▶ PlayStep+ EnqueueConsumer: healthyReset

Queue (badge = delivery attempts)

1

2

3

Consumer

idle

Dead-letter queue

empty

Processed

0

Press play. The consumer pulls one message at a time.

Flip the consumer to failing: unacked messages are redelivered, and after 3 attempts they land in the dead-letter queue instead of blocking the line. At-least-once delivery is why consumers must be idempotent.

If processing fails, the consumer does not send an acknowledgment. The queue then re-delivers the message to another consumer. This behavior is called at-least-once delivery: a message can arrive more than once, but a consumer failure does not lose it.

Dead letter queues handle poison messages, which are messages that fail every time they are processed. After several failed attempts, the message moves to a dead letter queue for manual inspection (shown in the widget above), so a broken message does not block the queue indefinitely.

FIFO (First In First Out) queues preserve message order, so order messages for the same user process in sequence. Standard queues allow out-of-order processing in exchange for higher throughput.

For more on message queues, event streaming, and asynchronous communication patterns, see Message Queue Fundamentals.

#### Common Implementations

RabbitMQ is a traditional message broker that supports complex routing. Its exchange types route messages to multiple queues in flexible ways, which suits systems that need detailed message routing and acknowledgments.

Apache Kafka is a distributed event streaming platform designed for high throughput. It handles millions of messages per second and retains them for replay. Common uses include event sourcing, real-time analytics, and log aggregation.

AWS SQS is a fully managed queue service, so there are no queue servers to operate. It scales automatically with message volume. Use it for cloud-based applications that value simplicity over advanced features.

### API Gateway

#### The Problem

A mobile app talks to 12 microservices: User Service, Order Service, Payment Service, Inventory Service, Notification Service, and more. Each service has a different authentication method. The mobile app must manage 12 API endpoints, 12 authentication schemes, and 12 retry strategies, and the client code grows complex.

Loading the home screen requires calls to 5 services: Users, Products, Recommendations, Cart, and Notifications. The mobile app makes these as 5 sequential HTTP requests. If each one takes about 100ms, the screen waits about 500ms before it loads.

Meanwhile, a malicious user sends 10,000 requests per second to the Order Service. With no rate limiting in place, the service crashes, and legitimate users cannot place orders.

An API gateway sits between clients and microservices and gives clients one endpoint to call. The gateway routes each request to the correct service, handles authentication in one place, enforces rate limits, and aggregates multiple backend calls.

#### How API Gateways Work

Clients send all requests to the gateway at https://api.example.com. The gateway inspects the request path and method. GET /users/123 routes to User Service. POST /orders routes to Order Service.

The gateway enforces cross-cutting concerns, which are functions that every service needs:

- Authentication: verify JWT tokens before forwarding requests

- Rate limiting: allow 100 requests per minute per user, return 429 if exceeded

- Caching: cache product details for 5 minutes to reduce backend load

Request aggregation combines multiple backend calls into one. The mobile app requests GET /home. The gateway calls User Service, Product Service, and Cart Service in parallel. It merges the responses into one JSON payload and returns it to the app, so one request replaces three.

Load balancing distributes requests across multiple instances. If three Order Service instances run, the gateway routes requests round-robin: instance 1, instance 2, instance 3, instance 1...

Centralized logging records all API traffic in one place. The gateway logs request timestamps, response times, and error rates, which makes monitoring and debugging easier.

For more on API gateway patterns, authentication strategies, and rate limiting implementations, see API Design and Gateway Patterns.

#### Common Implementations

AWS API Gateway is fully managed and integrates with Lambda, DynamoDB, and other AWS services. It handles authentication, throttling, and caching automatically, and it is a common choice for serverless applications and AWS-centric architectures.

Kong is an open-source gateway built on NGINX. Its plugin system supports custom authentication, rate limiting, and transformations. Use it for self-hosted environments that need flexibility and extensibility.

NGINX Plus combines a reverse proxy with API gateway features. High-throughput applications use it when they need fine-grained control over routing and caching.

## Problem Decomposition Framework

System design problems often arrive as vague statements such as "Design Twitter" or "Design Uber." The first task is to decompose the statement into concrete technical requirements. Keywords in the problem statement serve as anchors, so the requirements come from the text and not from guesses about the interviewer.

The framework has three steps, and each one pulls a different type of information out of the problem description.

### Step 0: Verbs → Use Cases

Verbs reveal operations. "Users can post tweets" contains the verb "post." "Users view their feed" contains "view." Extract the verbs to identify use cases.

Common verbs map to CRUD operations: create, read, update, delete, search, notify, process. Each verb becomes a functional requirement.

Next, define what "correct" means for each operation. Does "post tweet" require deduplication? Should followers see tweets immediately or eventually? Must tweets persist forever? Each answer narrows a verb into a precise contract that the design must meet.

### Step 1: Nouns → Entities and Ownership

Nouns point to data models. "Users post tweets" contains two nouns, "users" and "tweets," and "users follow other users" adds a relationship entity.

List the entities and their relationships. For each entity, identify the source of truth. Who owns user profile data? Where do tweets live? Which service controls the follow relationship?

Ownership determines write authority. The User Service is the only writer of user profiles, and the Tweet Service is the only service that creates tweets. With one writer per entity, two services cannot issue conflicting writes, and each service marks a consistency boundary.

### Step 2: Adjectives → Constraints and Add-ons

Adjectives carry the non-functional requirements, and these requirements force architectural choices. In "instant notifications," the word "instant" calls for real-time push mechanisms or precomputation. A "highly available feed" needs replication and stateless services.

Common adjectives and their implications:

instant/realtime → push notifications, WebSockets, caching, precomputation

reliable → retries, idempotency, dead letter queues, write-ahead logs

highly available → replication, stateless services, health checks

auditable/secure → encryption, access control, audit logs, compliance

scalable → partitioning, read replicas, message queues, horizontal scaling

Each adjective adds components to the architecture. Add a component only when a specific constraint justifies it.

## Interview Step-by-Step

This section applies the decomposition framework to Design Twitter, a common system design problem.

### Step 0: Identify Use Cases from Verbs

The first step of the framework extracts verbs from the problem statement to find the operations.

The problem is "Design Twitter." What can users do? Users post tweets. Users view their feed. Users follow other users. Users like tweets. Users comment on tweets.

Extract the verbs: post, view, follow, like, comment. Each verb maps to a use case:

- Post: create a new tweet

- View: read individual tweets or feeds

- Follow: create a relationship between users

- Like: increment engagement counter on a tweet

- Comment: create a response attached to a tweet

Now define what "correct" means. Should the same tweet content posted twice create two separate tweets or deduplicate? Assume no deduplication unless the problem specifies it. Should followers see new tweets immediately? This depends on non-functional requirements covered in Step 2. Must deleted tweets be recoverable? Not required for this problem.

An interview usually lasts under an hour, so the design focuses on core operations, and five use cases are enough.

### Step 1: Identify Entities from Nouns

The nouns in these use cases give the entities and their relationships.

From "users post tweets," we get User and Tweet. From "users follow other users," we get a Follow relationship. From "users like tweets" and "users comment on tweets," we get Like and Comment (both are types of engagement).

List the entities:

- User: represents an account with profile information

- Tweet: represents a message with content, timestamp, and author

- Follow: represents the relationship between follower and followee

- Engagement: represents interactions (likes and comments) on tweets

For each entity, establish ownership:

- User entity: owned by User Service, stored in User Database

- Tweet entity: owned by Tweet Service, stored in Tweet Database

- Follow entity: owned by Follow Service, stored in Follow Database

- Engagement entity: owned by Engagement Service, stored in Engagement Database

If two services could update the same tweet, the system would need a rule to decide which write wins. Making the Tweet Service the single source of truth removes that conflict, because all tweet writes go through one service.

### Step 2: Identify Constraints from Adjectives

Step 2 turns adjectives into non-functional requirements and their architectural implications.

The problem states Twitter should have "low latency" responses, "high availability," support "scalable" growth, and ensure "durable" storage. Extract the adjectives: low latency, highly available, scalable, durable.

Map each adjective to technical solutions:

Low latency: Suppose the target is a feed that loads in under 500ms. A database query on every feed request makes this target hard to meet, so the design needs caching. Precompute feeds, store them in Redis, and serve reads from the cache.

Highly available: The system must handle partial failures. If the Tweet Service crashes after it receives a post request, the tweet should not be lost. Buffering write requests in a message queue such as Kafka solves this, because messages persist while services are down and get processed when they recover.

Scalable: Suppose the service has hundreds of millions of monthly active users. A single server cannot handle this load. The design needs horizontal scaling, with load balancers that distribute requests across many service instances, and database partitioning that spreads data across shards.

Durable: Tweets must not be lost. Replicated databases store each record on multiple nodes, so the data stays accessible when one node fails.

Design checkpoint

An interviewer says the feed must be 'highly available' but never mentions latency. Which addition is justified first?

A cache, because caches always helpMessage queues and replication, because availability is about surviving partial failure

### API Design

API design follows the requirements and takes a few minutes. Each functional requirement becomes one API endpoint.

Check three things for each endpoint. Use readable paths, such as /tweet instead of /item. Know the data that each API sends and receives. Choose the correct HTTP method: POST to create, GET to fetch.

For Twitter:

The author comes from the authenticated session, so it does not appear in the request
body. Users post tweets:

POST/tweet

Request & response

Users view individual tweets:

GET/tweet/{id}

Request & response

Users view feeds:

GET/feed

Request & response

Users follow other users:

POST/follow

Request & response

Users like tweets:

POST/tweet/like

Request & response

Users comment on tweets:

POST/tweet/comment

Request & response

### High-Level Design

High-level design takes the largest part of the interview and combines the earlier steps with system design knowledge.

Steps 0, 1, and 2 produced the use cases, the entities, and the constraints. The architecture starts with a basic data flow for the use cases, and components for each constraint come after it.

Reading the diagrams below. Each step adds one component to solve one problem.
A pink NEW badge marks the component added at that step; everything else was
justified in an earlier step.

### Basic Data Flow

Map each API endpoint to the services its data passes through. Keep this first design minimal, with no complex parts, so the interviewer can correct a mistake early.

For microservices approaches, see Microservices and Monolithic Architecture.

For Twitter, each use case maps to a service in front of its own database: post
and read tweets, follow users, view feeds, like and comment:

This design has many services. Separation of concerns matters, but not every operation needs its own microservice, so look for services to combine. Likes and comments are both ways to engage with a tweet, and both are counters on tweets that hold different data. They merge into one Engagement Service with one Engagement Database.

With multiple services, add an API gateway (see Main Components section above).

### Applying Constraints

The basic data flow supports the use cases, but it fails at scale. The four constraints from Step 2 (low latency, high availability, scalability, and durability) each add the components they need, and each new component traces back to one of them.

Scalability is the most direct to address. Horizontal scaling adds service instances as traffic grows.

Each service (Tweet, Feed, Follow, and Engagement) runs as multiple instances. The instances operate independently and handle requests in parallel, with a load balancer in front to distribute traffic.

A load balancer spreads incoming requests evenly across the available service instances. Because it runs health checks on each instance and reroutes traffic away from unhealthy ones, it also supports high availability, a second non-functional requirement. Each service scales up or down with traffic. During peak hours, extra Feed Service instances absorb request surges, and they go away when activity drops.

Low latency comes next. With few users posting tweets, the servers respond quickly, and each feed fetches a handful of tweets. At millions of users and billions of tweets, a database read for every feed request becomes slow, and most of those reads fetch the same popular tweets again. A cache answers those repeated reads from memory.

A cache is fast storage that keeps frequently accessed data close to the application. The Feed Service can use a distributed cache such as Redis or Memcached to store recent tweets for each user.

When a user posts a tweet, the Feed Service updates the followers' feeds in the database. It also pushes the new tweet to the cache as part of each follower's precomputed feed. When a follower logs in, the Feed Service reads the feed from the cache. It does not query the database or aggregate the feed at request time.

Caches suit hot data, which is data that the system reads often, such as the latest tweets for user feeds. A cache holds data in memory, so it returns results in milliseconds.

Repeated reads go to the cache instead of the database. With less read load, the database keeps capacity for write operations, and the system can scale further.

To keep the cache fresh, set expiry times on cached items or use event-driven updates. With event-driven updates, each new tweet triggers a cache update, so followers see the latest tweets without delay.

Health checks on the load balancer cover one kind of failure, but other failures also affect high availability. A user posts a tweet at 1:02pm, and the tweet service goes down at 1:03pm. At 1:04pm, the user's followers open the app, and the tweet does not appear in their feeds. A different failure happens when millions of active users publish tweets at the same time, and processing all of them at once overloads the servers. A message queue handles both.

A message queue is a buffer between services. It decouples them and keeps messages, such as new tweets, when a service goes down. When a user posts a tweet, the Tweet Service places the tweet in the queue and does not call the Feed Service directly. Consumers read from the queue and write each tweet to both the database and the cache. The Feed Service reads from this cache to build user feeds. If the Tweet Service goes offline, the queue still holds the tweets, and consumers process them. The Feed Service can still update followers' feeds when they log in.

Message queues provide eventual consistency and keep the system available during partial failures. In the 1:02pm scenario, followers still see the tweet because the queue kept the message while the Tweet Service was down. The queue also absorbs changing workloads and traffic spikes, so the downstream services do not overload and can scale on their own.

With the service-level requirements covered, data durability remains. A system that holds billions of tweets, likes, and follows has no way to rebuild a record after the only copy is gone. Distributed databases prevent this loss by keeping more than one copy.

A distributed database replicates data across multiple nodes in a cluster. If one node goes down, the data stays accessible from the other replicas. Replication does not protect against a failure that hits every node, so regular snapshots of Tweet DB, Follow DB, and Engagement DB go to separate backup systems. After a total failure, the data is restored to its last consistent state.

### Deep Dives

Deep dives are the last step of a system design interview. They go past the high-level architecture into specific challenges and edge cases, and they test knowledge of advanced features, domain-specific scenarios, and trade-offs.

### How would you handle the Celebrity Problem?

The celebrity problem occurs when a user with millions of followers posts a tweet. The system must add that tweet to millions of follower feeds, which is a large fan-out. This load can cause high latency and high write amplification.

Push (fan-out-on-write) copies each post into every follower's timeline. In the
hybrid strategy, an author above a follower threshold switches to pull
(fan-out-on-read), and a viral post from that author makes zero timeline writes.

Pure pushHybrid (T = 100K)

Producer followers6K

Strategy for this author

Push on write

Timeline writes per post

6K

Push copies this post into 6K timelines at write time, so reads stay cheap.

Normal users with a manageable number of followers keep standard fan-out-on-write, so their tweets go to followers' feeds as soon as they post.

For users with large follower counts (more than 10,000), switch to fan-out-on-read. The system stores celebrity tweets in the Tweet Database and the Tweet Cache, but it does not precompute them into each follower's feed. When a follower opens a feed, the Feed Service fetches the celebrity's latest tweets from the cache or database. It then merges them into the user's timeline.

Set thresholds, by follower count or engagement volume, to choose fan-out-on-write or fan-out-on-read for each user.

What separates answers on celebrity fan-out

BadPure fan-out-on-write for everyone▾

GoodHybrid push/pull with a follower threshold▾

GreatHybrid, plus a cache for the pulled hot keys▾

### How would you efficiently support Trends and Hashtags?

Trends and hashtags need real-time aggregation across billions of tweets to find popular topics, and the aggregates must update often without overloading the system.

Each region or data center computes local trends. It aggregates hashtags and keywords with sliding window algorithms over a recent period, such as the past 15 minutes. Each region sends its local results to a global aggregation service, which combines them into global trends.

Change the Tweet Service to index hashtags when it creates a tweet. Keep an inverted index in which each hashtag is a key and its tweet IDs are the values. Store and query the hashtag indexes in a distributed search engine such as Elasticsearch or Solr.

Compute trends on a schedule, such as every minute, and store them in a distributed cache such as Redis for low-latency reads. A TTL (time-to-live) on each entry makes stale trends expire, so readers get fresh results without extra load.

### How would you handle Tweet Search at Scale?

Users search for tweets, hashtags, and profiles, and the search must scale and return results in real time. That calls for a distributed search architecture.

Change the Tweet Service to send new tweets to a search indexing service through a message queue. The indexing service processes the tweets and updates the search indexes in a distributed search engine such as Elasticsearch or Apache Solr.

Partition the search indexes by time (daily indices) or by hashtag to spread load across multiple nodes. Store older indices on slower, cheaper storage, and keep recent indices on faster nodes.

Use inverted indexes for keyword and hashtag search. Apply ranking algorithms (BM25 or ML-based) to return the most relevant tweets by user engagement, recency, or other factors.

A cache for popular search queries and their results reduces load on the search engines.

### Test Your Understanding

System Design Primer Quiz

Hide AllReveal All

1)Why should you reveal architecture components one at a time in an interview instead of drawing the full diagram up front?

Show Answer

2)Plain hash-mod-N sharding and consistent hashing both spread keys across nodes. Why prefer consistent hashing when the cluster resizes?

Show Answer

3)During a network partition, what does an AP system do that a CP system does not?

Show Answer

4)Two clients increment the same counter concurrently and one update is lost. How does optimistic locking prevent this?

Show Answer

5)Why does a message queue require workers to be idempotent?

Show Answer

Explain

Add to Chat

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

Was this lesson clear?

👍👎

### How to Solve Any System Design Interview

#### Comments

Join the Discussion

Dean Hunter

Thank you very much for this. I have learnt a great deal. I would like the primer to include more on the deep dive including patterns than the specific example for Twitter. Great course overall.

Sun Jul 12 2026

Michael Moon (Michael)

Amazing content

Tue Jun 09 2026

1

falase femi

very well detailed

Wed Apr 01 2026

Pawan Pawar

Well written primer! 👏🏻

Fri Jan 02 2026

Manjunath A

Every helpfull

Fri Nov 28 2025

mohan nair

How is the GET request for tweets returning the likes and comments since those are stored in Engagement DB as per the HLD?
GET /tweet/<id>

Wed Sep 24 2025

PLuna

This is awesome. Thank you so much for posting this. One thing that confuses me is how to get good at the API Design part. Aside from your tips, for someone thats never written GET, POST or PUT requests, how do we know how to write those for the first time?

Thu Jul 31 2025

1

Don Mamaril

This was an excellent primer. Thank you!

Sun Jul 20 2025

Ank7T

"What happens if a user posts a tweet at 1:02pm, but at 1:03pm, our tweet service goes down, and at 1:04pm, their followers log onto the app. Are their followers going to see this tweet in their feed? As it stands now, NO!"

But as per the design, when a user posts a tweet it also gets added into follower's feed cache. so even if tweet service goes down, other users should be able to see the tweet in their feed.

Thu Jun 12 2025

1

Mosharaf Hossain

Supper nice explanation - short, sweet, and to the point. Thank you

Tue Jun 10 2025

2

Load More

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

IntroductionWhat Is System Design?System Design vs Object-Oriented DesignWhat Are System Design Interviews?What System Design Interviews TestLevel ExpectationsHow to PrepareWhy Memorized Solutions Fall ShortHow to Study InsteadWhat the Primer and the Course CoverWhere to StartHow This Primer Is OrganizedCore Design ChallengesChallenge 1: Too Many Concurrent UsersChallenge 2: Too Much Data to Move AroundChallenge 3: The System Should be Fast and ResponsiveChallenge 4: Inconsistent (outdated) StatesDesigning for ScaleEstimating the LoadDecompositionVertical ScalingHorizontal ScalingPartitioningCachingBuffer with Message QueuesSeparating Read and WriteCombining TechniquesAdapting to Changing Business RequirementsConsistency and TradeoffsThe CAP TheoremConsistency ModelsContention and ConcurrencyMulti-Step Workflows and SagasMaster TemplateComponent BreakdownDataflow PathMain ComponentsMicroservicesRelational DatabasesNoSQL DatabasesObject StorageCacheCDN (Content Delivery Network)Message QueuesAPI GatewayProblem Decomposition FrameworkStep 0: Verbs → Use CasesStep 1: Nouns → Entities and OwnershipStep 2: Adjectives → Constraints and Add-onsInterview Step-by-StepStep 0: Identify Use Cases from VerbsStep 1: Identify Entities from NounsStep 2: Identify Constraints from AdjectivesAPI DesignHigh-Level DesignBasic Data FlowApplying ConstraintsDeep DivesHow would you handle the Celebrity Problem?How would you efficiently support Trends and Hashtags?How would you handle Tweet Search at Scale?Test Your Understanding

Read0%

Need help?Ask about this section

On this pageIntroduction0%

Send feedback
