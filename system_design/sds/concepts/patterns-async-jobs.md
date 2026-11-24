---
layout: simple
title: "Asynchronous Jobs Pattern — System Design School"
permalink: /system_design/sds/concepts/patterns-async-jobs
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

# Asynchronous Jobs: Accept, Enqueue, Return

mediumAsync processingMessage queueIdempotency

Some work is too slow to finish inside a request. Transcoding a video into several resolutions, generating a large report, or sending a batch of thousands of emails can each take minutes. If the request handler does that work inline, the connection stays open the whole time, and a gateway or proxy usually cuts it off after 30 to 60 seconds. The caller sees an error even when the work was progressing fine.

Holding the connection open also pins a request thread that could serve other users, and ties the caller's experience to the slowest step in the chain. The way out is to stop doing the slow work inside the request at all.

## The pattern: accept, enqueue, return

The fix is to stop doing the slow work inside the request. Accept the request, record that work is pending, hand the slow part to a background process, and answer the client immediately. The response is 202 Accepted: the server took the request but has not finished it. It carries a job id the client uses to track progress.

202 Accepted. An HTTP status meaning the request is valid and queued, but processing is not done. Unlike 200 OK, it promises nothing about a result yet. The body typically returns a job id and a status URL.

Three components make this work.

The first is a durable queue: a store that holds job records until a worker claims one. Durable means the queue survives a crash; an enqueued job is not lost if a broker restarts. The queue also absorbs bursts, holding a spike of jobs that arrive faster than workers can process them. (For the mechanics of the queue itself, see Message Queue.)

The second is a worker pool: processes that pull jobs from the queue and run them. Workers are separate from the API servers. They do the transcoding, report building, or email sending on their own machines, at their own pace.

The third is a job-status store: a small record per job holding its state — queued, running, done, or failed — plus the result or an error. The API server writes the initial queued row. The worker updates it as the job progresses. The client reads it to learn the outcome.

The upload handler now does three cheap things: store the raw file, write a queued status row, and enqueue a transcode job. It returns 202 with the job id in milliseconds. The transcode happens later, off the request path. This is a form of two-stage processing: accept fast, process later.

Key idea. Slow work does not belong on the request thread. Accept the request, enqueue a job, and return a job id so the client can check back.

## How the client learns the result

The client holds a job id but no result yet. Two mechanisms close that gap, and they trade wasted work against setup cost.

Polling is the client asking. It calls GET /v1/jobs/{id} on a timer — say every two seconds — until the status turns done or failed. Polling is simple and needs nothing special from the client. The cost is wasted requests: most polls return running and learn nothing. There is also lag, up to one poll interval, between the job finishing and the client noticing.

A webhook is the server telling. The client registers a callback URL once. When the job finishes, the system sends an HTTP request to that URL with the result. No wasted polls, and the client hears the moment work completes. The cost is setup: the client must expose a reachable endpoint, and the server must retry the callback if it fails, since the client might be briefly down.

The choice follows the client. A browser cannot easily receive a webhook, so it polls, or uses a push transport like Server-Sent Events (covered in Real-Time Transport). A server-to-server integration usually prefers a webhook to avoid the polling waste. Many systems offer both.

Key idea. Polling wastes requests but needs no client setup; webhooks are efficient but require a reachable, retried callback. Match the mechanism to whether the client can receive a push.

## Why this absorbs spikes

Decoupling the slow work also changes how the system handles load. On the synchronous path, a spike of uploads competes directly with every other request for the same threads. Ten times the normal traffic means ten times the transcoding load on the servers answering users. Latency climbs for everyone.

With a queue in the middle, the enqueue is cheap and constant. A burst of uploads writes a burst of jobs into the queue in milliseconds each. The user-facing path stays fast because it never runs the heavy work. The queue holds the backlog. Workers drain it at their own steady rate, and the backlog shrinks once the spike passes.

This is why the design scales writes. Throughput is set by the worker pool, not the API tier, and the two scale independently. If transcoding falls behind, add workers; the API servers are untouched. If request volume grows, add API servers; the workers are untouched. The queue length becomes a visible signal — a growing backlog means workers are under-provisioned. YouTube's upload pipeline follows exactly this shape, worked out in full in the Design YouTube solution.

Key idea. The queue turns a spike into a backlog. Workers set throughput and scale on their own, so bursts never slow the request path.

Design checkpoint

A worker pulls a transcode job, spends two minutes on it, and crashes right before it reports success. The job was never marked done. What guarantees the video still gets transcoded?

Nothing — the job is lost when the worker diesThe queue redelivers the job because it was never acknowledgedThe API server retries the original upload request

## Reliability: at-least-once and idempotency

A queue that could lose jobs on a crash would be useless for real work. So queues delay removing a job until a worker confirms it finished. This gives at-least-once delivery: every job runs at least once, but some run more than once.

At-least-once delivery. The queue guarantees a job is not lost, at the cost of possible repeats. If a worker processes a job and dies before acknowledging it, the queue cannot tell "done" from "crashed," so it redelivers. The alternative, at-most-once, acknowledges first and can silently drop work — worse for jobs that must happen.

Repeats are the price of not losing work. A transcode that runs twice wastes CPU but is otherwise harmless. A job that sends a payment or an email is different: running it twice charges the user twice or sends a duplicate. The worker must be idempotent so a repeat causes no extra effect.

Idempotency. An operation is idempotent when running it many times leaves the same result as running it once. The common technique is to key the side effect on the job id. Before sending the email, check whether job_id is already recorded as sent; if so, skip. The second run becomes a no-op.

Idempotency is what makes at-least-once safe. Without it, redelivery corrupts data. With it, redelivery is just a retry. This same reasoning drives saga patterns, where each step of a multi-service workflow must be safely retriable.

### Retries, backoff, and the dead-letter queue

Jobs fail for reasons that are not a crash: a downstream service is briefly down, a network call times out, a file is momentarily locked. Most of these are transient. Retrying usually works.

Retrying immediately does not. If a downstream service is overloaded, a wave of instant retries adds load and keeps it down. Retries use exponential backoff: wait a short delay, then double it each attempt — 1s, 2s, 4s, 8s — with a little random jitter so many workers do not retry in lockstep. Backoff gives the failing dependency room to recover.

Some jobs fail no matter how many times they run. A malformed video file will never transcode. A job pointing at a deleted record will always error. These are poison jobs. Retrying them forever wastes workers and hides the failure. So retries have a cap. After a fixed number of attempts, the job moves to a dead-letter queue (DLQ): a separate queue for jobs that exhausted their retries.

The DLQ keeps a bad job from clogging the pipeline behind healthy ones and from failing silently. An alert fires on DLQ depth, an engineer inspects the job, fixes the cause, and can replay it. Nothing is lost, and nothing loops forever.

Key idea. At-least-once delivery means jobs can repeat, so workers must be idempotent. Transient failures retry with exponential backoff; poison jobs stop at a dead-letter queue for a human.

## What a strong answer sounds like

How do you handle video transcoding when a user uploads a file?

BadTranscode inside the upload request▾

GoodEnqueue a job and return 202▾

GreatIdempotent workers, retries, DLQ, independent scaling▾

## The transferable pattern

Any request that triggers slow or spiky work follows this shape. Do the cheap part synchronously — validate, store, record a pending status — then enqueue the heavy part and return a job id. A durable queue holds the backlog, a worker pool drains it at its own rate, and a status store carries the outcome back to the client. Because the queue delivers at-least-once, the worker must be idempotent; because dependencies fail, retries use backoff and a dead-letter queue catches what never succeeds.

Two system designs extend this pattern. A distributed job scheduler decides when queued work becomes eligible and recovers jobs whose leases expire, while a LeetCode-style online judge runs each queued submission inside a restricted sandbox with enforced resource limits.

Transcoding, report generation, bulk email, image processing, data exports, and payment settlement all reduce to this. The moment a request's work outlives the request, move it off the thread and behind a queue.

Key idea. When work outlives the request, accept fast and process behind a durable queue. Idempotent workers plus backoff and a dead-letter queue turn at-least-once delivery into a reliable pipeline.

## Sources and further reading

- Amazon SQS dead-letter queues — AWS docs — how a DLQ isolates messages that exhaust their retry limit.

- Designing robust and predictable APIs with idempotency — Stripe — keying side effects on a request id so retries are safe.

- Best practices for using webhooks — Stripe docs — reachable callback endpoints and retrying failed deliveries.

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

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

The pattern: accept, enqueue, returnHow the client learns the resultWhy this absorbs spikesReliability: at-least-once and idempotencyRetries, backoff, and the dead-letter queueWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageThe pattern: accept, enqueue, return0%

Send feedback
