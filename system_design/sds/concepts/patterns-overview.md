---
layout: simple
title: "The 10 System Design Patterns — System Design School"
permalink: /system_design/sds/concepts/patterns-overview
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

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time TransportHandling Large Files

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# System Design Patterns: The 10 That Solve Most Problems

easyScalability

The solutions on this site cover 37 interview problems, such as Twitter, YouTube, Uber, a payment system, and a chat app. Side by side, they use the same patterns again and again. About ten patterns cover almost all of them, and each problem uses a few. So a new problem is mostly a question of which patterns it needs.

Each pattern fixes one kind of failure. The video below builds one photo-sharing app from a single server. Each time something breaks, the next pattern fixes it. This page is the written version. Each section below names the failure, the pattern, and its main techniques, then links to the page that teaches it in depth.

## 1. Scale Reads

Most apps read much more than they write. One post is written one time and viewed many times. So the first part to struggle is usually the database, which answers the same queries again and again.

Reads scale by copying the data. A cache in memory answers repeated reads before they reach the database. Read replicas copy the database so that more machines share the reads. A CDN copies static files to servers near the users. The cost is that a copy can be slightly stale. (Scaling Reads and Writes)

## 2. Scale Writes

Every write still goes to one primary database. At some point, one machine cannot accept the writes, or the data no longer fits on it.

Writes scale by splitting the data. Sharding puts each part of the data on a different database. The shard key decides which part goes where. A good key spreads the load evenly. A bad key, such as the creation date, sends all new writes to one shard. (Scaling Reads and Writes, Database Partitioning)

## 3. Move Slow Work to a Queue

Some work takes seconds or minutes, such as converting an uploaded video. If the request waits for that work, the user waits, and the servers fill up with waiting requests.

The server puts a job on a message queue and answers at once. Separate workers take jobs from the queue and do the work at their own speed. A burst of jobs makes the queue longer but does not overload the servers. Failed jobs retry with backoff, and jobs that keep failing go to a dead-letter queue. (Asynchronous Jobs)

## 4. Fan-out

A feed shows recent posts from the accounts that a user follows. There are two ways to build it.

Fan-out on write copies each new post into the feed of each follower when it is posted, so reading a feed is fast. Fan-out on read builds the feed when the user opens it, so posting is cheap but reading is slow. An account with millions of followers makes fan-out on write too expensive. So most designs use a hybrid: push posts from normal accounts, and pull posts from very large accounts at read time. (Push vs Pull)

## 5. Hot Keys

A popular item sends most of the traffic to one key, and one key lives on one server. That server does most of the work while the others are idle. This is a hot key.

For reads, store several copies of the hot entry on different servers, and let each reader pick one. For writes, such as likes on a viral post, split the counter into several sub-counters and add them up when it is read. (Distributed Caching)

## 6. Count at Scale

Likes, views, and ad clicks can arrive much faster than a database can write them one by one.

Batching adds up counts in memory and writes the total at intervals, at the risk of losing the last interval in a crash. Windowed aggregation counts events per time window in a stream processor. When an exact count costs too much, probabilistic data structures give a close estimate in a small amount of memory: a count-min sketch for frequencies, and HyperLogLog for unique counts. (Windowing Patterns, Probabilistic Data Structures)

## 7. Large Files

A large file that goes through the application servers occupies a server for the whole upload, and the file does not end up there anyway.

The file goes to object storage, and the database keeps only its metadata. A presigned URL lets the client upload directly to object storage for a short time. Large uploads go in chunks, so a failed chunk can restart without the whole file. A CDN serves the files to readers. (Handling Large Files)

## 8. Real-time Updates

A normal request lets the server answer only when the client asks. A chat message must reach the receiver without that request.

Long polling holds a request open until there is news. Server-Sent Events keep one open connection for messages from the server to the client. A WebSocket keeps one connection open for messages in both directions, which suits chat. Each server then has many open connections, so the system must track which server holds each user's connection. (Real-Time Transport)

## 9. Special Indexes

A normal database index cannot answer some queries well. Text search and location search are the two common cases.

An inverted index maps each word to the list of documents that contain it, so a search goes straight to that list. A geohash turns a location into a short string, and nearby places share the start of that string. A quadtree splits a map into smaller cells where there are many points. Both let a "nearby" query check only a few cells. (Inverted Index, Geospatial Search)

## 10. Handle Failure

In a large system, some part is usually failing. A slow service can make every service that calls it slow too.

A timeout stops a call from waiting forever. A retry with backoff tries again after a delay. A circuit breaker stops calls to a failing service for a while and returns a fallback. Rate limiting stops one client from using more than its share, often with a token bucket. (Timeouts, Circuit Breaker, Rate Limiting)

## Which Problems Use Which Patterns

Most problems need only a few of the ten patterns. Finding them early is a large part of the interview.

ProblemMain patterns

YouTubeMove slow work to a queue, Large files, Scale reads (CDN)

News feedFan-out, Hot keys, Scale reads

Chat appReal-time updates, Fan-out, Move slow work to a queue

UberSpecial indexes, Scale writes, Hot keys

Top KCount at scale, Scale writes

Rate limiterHandle failure, Hot keys

URL shortenerScale reads, Scale writes

Key idea. About ten patterns cover most system design problems. Each pattern fixes one kind of failure and has a cost. A strong design names the failure first, then picks the pattern that fixes it.

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

Mosharaf Hossain

Thank you for summarizing this! I was waiting for it - appreciate for both the new videos of a new template and the 10 valuable patterns.

Thu Nov 05 2026

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

1. Scale Reads2. Scale Writes3. Move Slow Work to a Queue4. Fan-out5. Hot Keys6. Count at Scale7. Large Files8. Real-time Updates9. Special Indexes10. Handle FailureWhich Problems Use Which Patterns

Read0%

Need help?Ask about this section

On this page1. Scale Reads0%

Send feedback
