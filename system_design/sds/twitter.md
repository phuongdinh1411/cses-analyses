---
layout: simple
title: "Design Twitter — System Design School"
permalink: /system_design/sds/twitter
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

LeetCode (Online Judge)Typeahead / AutocompleteDistributed Rate LimiterTicketmasterNews FeedUber / Nearby DriversYouTubeNetflixChat App (WhatsApp / Messenger)TinderGoogle CalendarInstagramGoogle DocsDropboxLocal Delivery (Gopuff)Live Comments (Real-Time Fan-Out)News AggregatorDistributed CachePub-Sub / Message QueueTop K (Trending)Web CrawlerPost Search (Full-Text Search)Distributed Job SchedulerDistributed Key-Value StoreMetrics Monitoring SystemPayment SystemRobinhood (Stock Trading)Online AuctionAd Click AggregatorURL ShortenerPastebinYelpTwitterGoogle MapsWebhook

AI System Design6

RAG SystemChatGPTImage Generation ServiceCoding Agent CLI (Claude Code)

Show all 6 →

Patterns5

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time Transport

Show all 5 →

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# Design Twitter

Fan-outCachingCelebrity problem

Practice this problem

ScopeHLDE2EScalingCapacity

We aim to design a simplified version of Twitter, a popular social media platform where users can post tweets, follow or unfollow other users, and view the tweets of the people they follow. The platform also includes a recommendation algorithm that suggests content to users based on their preferences and interactions.

## Functional Requirements

Practice this problem: Functional Requirements

- Tweeting: Users should be able to write and post new tweets.

- Follow/Unfollow: Users should have the ability to follow or unfollow other users.

- Timeline: Users should be able to view a list of tweets from the people they follow, as well as content recommended by the recommendation algorithm.

## Non-Functional Requirements

Practice this problem: Non-Functional Requirements

- 300M DAUs

- Each tweet is approximately 140 characters (or 280 bytes)

- Retain data for five years.

- Assuming each user posts one tweet per day.

- High availability

- Low latency

- High durability

- Security

## Resource Estimation

Practice this problem: Resource Estimation

Assuming a read-write ratio of 100:1.

Using the resource estimator, we get the following results:

## API Endpoint Design

The API endpoints could include:

- POST /tweets for creating a new tweet. Request body as below:

{
"content": "The content of the new tweet."
}

- GET /tweets/{userId}?last={timestamp}&size={size} for retrieving a user's tweets.

- POST /follow/{userId} for following a user.

- DELETE /follow/{userId} for unfollowing a user.

- GET /timeline?last={timestamp} for retrieving timeline tweets.

## High-Level Design

Practice this problem: High-Level Design

This design applies the system design template.

The system splits into three services: the Tweet Service, the Follow Service, and the Timeline Service.

The Tweet Service and Follow Service handle writes — posting a tweet, following, unfollowing. Neither writes to the database on the request path. Each request is appended to a message queue and acknowledged immediately, so the client waits only for the enqueue, not for the database write and cache update behind it. A Database Updater consumes the queue, applies the business logic, writes to the database, and updates the cache.

Deferring the write this way has consequences that shape the rest of the design:

- The acknowledgement is not durability. The client gets a 202-style response once the tweet is queued. If the Database Updater is behind, the tweet exists in the queue but not yet in any timeline.

- Delivery is at-least-once. A consumer that crashes after writing but before acknowledging will reprocess the message. The Database Updater must be idempotent — key the write on the tweet ID so a replay overwrites rather than duplicates.

- Read-after-write is not guaranteed. A user may not see their own tweet immediately after posting. The usual fix is to write the author's own copy synchronously, or to render it optimistically on the client.

The Timeline Service handles reads. It serves from the cache rather than the database, because a timeline read is the highest-volume operation in the system at a 100:1 read-write ratio.

How the Timeline Service assembles a response is the substance of the design, and the next two sections derive it: fan-out places followed tweets into the inbox at write time, and a separate path supplies recommended content.

### Fan-out-on-write

Each user has their own "inbox" inside the cache that stores the tweets to be displayed in its timeline. When a user it follows posts a tweet, the tweet is sent to its "inbox". This is often called "fan-out-on-write" because it replicates ("fans out") a piece of information to multiple destinations at the time of its creation or update. The advantage of this is it reduces read latency, since the tweets are already present in a timeline cache when a user logs in. It reduces the need for complex and time-consuming queries at the time of read. However, for celebrities with millions of followers this could present a problem as the write would be quite large. The follow-up question section covers the mitigation.

### Recommended Content

Fan-out fills the inbox with tweets from accounts the user follows. The third functional requirement also calls for recommended content — tweets from accounts the user does not follow. These cannot be pushed at write time, because there is no follower edge to fan out along.

Recommendations are served on a separate path with three stages:

Candidate generation produces a few hundred plausible tweets from a corpus of millions. Cheap retrieval strategies run in parallel: tweets engaged with by accounts the user follows, tweets on topics the user has recently interacted with, and tweets trending in the user's region. Each strategy is an index lookup rather than a scan.

Ranking scores those candidates with a model over features such as recency, engagement rate, author affinity, and topic match, then keeps the top few dozen. Scoring a few hundred candidates is affordable; scoring millions is not, which is why candidate generation runs first.

Merging interleaves the ranked recommendations with the inbox tweets at read time. Recommendations are injected at a fixed ratio — for example one recommended tweet every five followed tweets — rather than sorted purely by score, so the timeline stays recognisably chronological and a high-scoring recommendation cannot crowd out followed accounts.

Ranking runs off the request path where possible. A periodic job precomputes and caches each active user's ranked recommendation set, so a timeline read is two cache lookups plus a merge rather than a live model inference. The analytics component described below supplies the interaction data these models train on.

### The Composed Design

Every component is now established: the two write services and the queue behind them, the Database Updater that drains it, the inbox that fan-out fills, the recommendation path, and the Timeline Service that merges the two at read time. Together they form the following design.

## Detailed Design

### Database Type

Considering the scale requirement of 300M DAU and assuming that each user sends one tweet per day, this would generate 300M tweets per day. At 280 bytes per tweet that is roughly 84 GB of tweet text per day, or about 153 TB over the five-year retention window before replication. At the same time, this system does not have complex query requirements. Considering these two points, NoSQL could be used as the database.

Cassandra is a reasonable choice because its characteristics constrain the schema design.

The write path is append-only and skips the read. A write is routed by hashing its partition key to a position on a ring of nodes. The receiving node never reads the existing row first. It writes to two structures, then acknowledges:

- Commit log — an append-only file on disk. Every write is appended to its end before the write is acknowledged, so if the node loses power the log can be replayed to recover writes that had not yet reached their permanent home. Appending to the end of a file is a sequential disk operation, which is far cheaper than seeking to a specific location to modify a record in place.

- Memtable — a sorted table of recent writes held in memory. Once it fills, it is flushed: written out as a new immutable file on disk, sorted by key. Flushed files are never modified afterwards.

Because flushed files are immutable, an updated row does not overwrite the old one — it lands in a newer file, and the old version stays where it is. Reads therefore consult several files and take the newest version of the row. Left alone, the number of files would grow without bound, so a background process called compaction periodically merges several files into one, keeping the newest version of each row and discarding superseded copies.

Contrast this with an update-in-place engine, the model a traditional relational database uses: the row occupies a fixed location on disk, and an update seeks to that location and rewrites it. Modifying one small field can force the engine to read, modify, and rewrite a whole disk page — and often to update index pages too. The ratio of bytes actually written to disk against bytes the application asked to write is called write amplification, and in that model it is well above one.

A concrete pass through the path — three writes to the same tweet row:

- INSERT t9 — appended to the commit log, inserted into the memtable. Acknowledged. No disk seek, no read.

- Memtable fills → flush produces immutable file F1 containing t9.

- UPDATE t9 (say, an edited body) — appended to the log and the new memtable, later flushed as F2. F1 still holds the stale copy; a read of t9 now checks F2 first and returns its version.

- Compaction later merges F1 and F2 into F3, keeping only the newer t9 and dropping the stale one.

The disk operation on the request path is a sequential commit-log append; the memtable is updated in memory. The merging work is deferred to step 4, off the request path, which is why the write path absorbs a steady ~3,500 tweets per second without paying the write amplification an update-in-place engine would incur on each write.

Replication is leaderless. Each partition is stored on N nodes (a replication factor of 3 is common), and no single one of them is the designated primary. Any replica can accept a write. Consistency is chosen per query rather than fixed by the engine: a write at quorum acknowledges once 2 of 3 replicas confirm, so one node can be down or partitioned and the write still succeeds. That maps onto the high-availability requirement — the tweet path stays writable through a node failure, at the price of replicas that briefly disagree until the write propagates.

The schema is driven by queries, not by entities. Cassandra has no joins, and a query that does not specify a partition key must scan every node. Tables are therefore built one per access pattern, duplicating the same rows across them. Storing tweets once and joining at read time is not an option; each way the application needs to read tweets becomes its own table. The schema and partitioning sections that follow work through what that produces.

A concrete pair of operations shows the shape. Suppose tweets are stored twice — once keyed on TweetID, and once on (UserID, TweetTimestamp):

- Write — posting tweet t9 by user u4 inserts the row into both tables. The Database Updater performs both inserts, and because each row is keyed on TweetID, a redelivered message overwrites rather than duplicating.

- Read — loading u4's profile issues a single query against the (UserID, TweetTimestamp) table with UserID = u4. It touches one partition on one set of replicas, returns rows already sorted by timestamp, and performs no join.

The cost of this model is that a new access pattern means a new table and a backfill, and that the duplicated copies are only eventually consistent with each other. For this workload — few query shapes, all known in advance, and a read path that never needs an ad-hoc join — that trade is acceptable.

### Data Schema

## Grasping the building blocks ("the lego pieces")

This part of the guide will focus on the various components that are often used to construct a system (the building blocks), and the design templates that provide a framework for structuring these blocks.

### Core Building blocks

At the bare minimum you should know the core building blocks of system design

- Scaling stateless services with load balancing

- Scaling database reads with replication and caching

- Scaling database writes with partition (aka sharding)

- Scaling data flow with message queues

### System Design Template

With these building blocks, you will be able to apply our template to solve many system design problems. We will dive into the details in the Design Template section. Here’s a sneak peak:

### Additional Building Blocks

Additionally, you will want to understand these concepts

- Processing large amount of data (aka “big data”) with batch and stream processing

- Particularly useful for solving data-intensive problems such as designing an analytics app

- Achieving consistency across services using distribution transaction or event sourcing

- Particularly useful for solving problems that require strict transactions such as designing financial apps

- Full text search: full-text index

- Storing data for the long term: data warehousing

On top of these, there are ad hoc knowledge you would want to know tailored to certain problems. For example, geohashing for designing location-based services like Yelp or Uber, operational transform to solve problems like designing Google Doc. You can learn these these on a case-by-case basis. System design interviews are supposed to test your general design skills and not specific knowledge.

## Working through problems and building solutions using the building blocks

Finally, we have a series of practical problems for you to work through. You can find the problem in /problems. This hands-on practice will not only help you apply the principles learned but will also enhance your understanding of how to use the building blocks to construct effective solutions. The list of questions grow. We are actively adding more questions to the list.

Pro Member Exclusive

Upgrade your account to continue

Benefits

Unlimited access to practice tool with AI grading

Unlimited access to expert-written solutions

Unlock 100+ lessons with full course access

Access to all future content while subscribed

Upgrade

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

Michał Dobrzański

You're missing an arrow from Read service to the Database. As some timeline might not be prepared yet.

Also this happens for the celebrity hybrid fan-out case, when users have not been active.

Mon Sep 22 2025

Jean-Christian Imbeault

For the timeline cache, mow many tweets does it hold? Is it able to go back years? Asking as this sounds like the timeline service will work well for going back days or weeks, but I can't imagine that it work if I wanted to go back 10 years ...

Fri Oct 18 2024

Sheldon Chi

Great question. If a user doesn't login for a while and becomes "dormant", the timeline cache may evict the entry. If it does become online again, we can do a pull to get his latest timeline.

Sat Oct 19 2024

Practice this problem

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

Functional RequirementsNon-Functional RequirementsResource EstimationAPI Endpoint DesignHigh-Level DesignFan-out-on-writeRecommended ContentThe Composed DesignDetailed DesignDatabase TypeData SchemaDatabase PartitioningDatabase ReplicationData Retention and CleanupCacheAnalyticsSecurityFollow Up Detailed Design Questions and AnswersReferences

Read0%

Need help?Ask about this section

On this pageFunctional Requirements0%

Send feedback
