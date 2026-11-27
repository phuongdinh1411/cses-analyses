---
layout: simple
title: "Design RAG System — System Design School"
permalink: /system_design/sds/rag
---

# Design a RAG System

**Difficulty:** Hard  
**Topics:** Vector search · Embeddings · Hybrid retrieval · Multi-tenancy · Async processing

## Problem statement

Design a retrieval-augmented generation (RAG) system for "chat with your data." A user asks a question in natural language. The system finds the passages in a private corpus that answer it and hands them, with their sources, to a language model that writes the answer. The corpus belongs to many tenants (customer organizations), holds on the order of 100 million documents, and changes all the time.

The scope is retrieval and grounding. The system ingests documents, keeps them searchable, and returns the best passages for each query, scoped to what the asker may see. Scope ends where the prompt is assembled. Serving the language model that writes the answer, training the embedding model, and multi-step agent loops are out of scope.

## Clarifying questions

Each question below is paired with the assumption its answer establishes.

- Is the corpus public or private? Private and per-tenant. A user must never retrieve a passage from another tenant or from a document they lack access to.

- How fresh must results be? A changed document must be retrievable within minutes. A deleted document must stop appearing immediately.

- What kinds of queries? Both meaning ("why do refunds fail?") and exact terms (a person's name, an order id, the error code E1042).

- Is the embedding model given? Yes. An embedding model is a pre-trained network that maps text to a fixed-length list of numbers (a vector) so that texts with similar meaning land close together. Training it is out of scope.

- How is the system sized? By the number of chunks — the passages documents are split into — since each chunk becomes one vector.

- Latency target? Retrieval is a small slice of the end-to-end answer time: tens of milliseconds at p99 (the slowest 1% of requests).

## What makes this problem distinctive

The obvious first idea is to paste the documents into the model's prompt. That does not work: the corpus is many orders of magnitude larger than any model's context window (the maximum text a model reads in one request). So the problem is not prompting. It is a search system over meaning, fed by a continuous ingestion pipeline.

Three tensions shape it. Finding the closest vectors exactly means comparing the query against every vector, which is far too slow, so the system must accept approximate answers and manage how approximate they are. Meaning-based search misses exact identifiers that keyword search catches, so retrieval quality needs more than one signal. And every result must belong to the asker's tenant and pass their permissions, which pulls directly against the efficiency of one shared index.

Vectors and dimensions. An embedding is a vector such as [0.12, -0.40, …] with a fixed length, for example 768 numbers. Each number is one dimension. Stored as 4-byte floats, a 768-dimension vector takes about 3 KB.

## Key concepts

This section covers the concepts needed to solve this problem — prerequisites for the design work that follows.

### Chunking and embedding

A 40-page manual is too large to embed as one vector: one vector cannot hold the meaning of every section, and the model would receive the whole manual for any question. So documents are split into chunks of a few paragraphs, often with a small overlap so a sentence at a boundary appears in both neighbors, and with the section header kept on each chunk. Each chunk is embedded into one vector. At query time the question is embedded with the same model, and the closest chunk vectors are the candidates.

### Approximate nearest neighbor search

Nearest neighbor search returns the stored vectors closest to a query vector. Done exactly, it compares the query with every vector. Approximate nearest neighbor (ANN) search uses an index that inspects a small fraction of vectors and usually finds the true neighbors, but not always. The fraction of true top-k neighbors it does return is called recall: if the exact top 10 and the ANN top 10 share 9 chunks, recall@10 is 0.9.

One common index, HNSW (Hierarchical Navigable Small World), links each vector to a handful of nearby vectors, forming a graph. A search starts at an entry node and repeatedly moves to whichever neighbor is closer to the query. It stops when no neighbor is closer. The widget below runs that walk on a single graph layer. Compare the distances it computes with a brute-force scan, and note that one query can stop at a near node that is not the nearest.

Query AQuery BQuery C▶ Walk the graphStepReset

Distances computed (graph walk)

1

Distances computed (brute force)

60

Result

walking…

Red diamond = query. Blue = current node and path. Orange = nodes whose distance was computed. Green = true nearest neighbor. The walk moves to whichever neighbor is closer to the query and stops when no neighbor is closer.

HNSW adds upper layers with fewer, longer links, so the walk crosses the space in a few hops before it descends to the dense bottom layer. The links cost memory on top of the vectors themselves.

### Keyword search and BM25

Vector search matches meaning, so "refund fails" finds "chargeback rejected." It is weak at exact strings: the vectors for E1042 and E1043 can sit almost on top of each other. Keyword search uses an inverted index — a map from each term to the list of chunks that contain it — and scores matches with BM25, a formula that rewards a term appearing often in a chunk and penalizes terms that appear in many chunks. (For a deeper dive, see Inverted Index Fundamentals.)

### Bi-encoders and cross-encoders

The embedding model is a bi-encoder: it encodes the query and each chunk separately, so chunk vectors are computed once at ingest and a query costs one embedding plus a vector lookup. That speed has a price. The model never sees query and chunk together, so its scores are approximate. A cross-encoder reads the query and one chunk together in a single pass and outputs a relevance score. It is sharper, but it must run once per (query, chunk) pair at query time, so it can only score a short list.

### Metadata filtering

Each chunk carries metadata: its tenant, the access-control list (ACL) of users and groups allowed to read its document, and fields like date and type. A query for tenant acme by user u42 must return only chunks whose tenant is acme and whose ACL admits u42. The filter is a predicate on metadata, applied together with the vector search.

Key idea. RAG retrieval is approximate search over chunk vectors, sharpened by keyword search and a cross-encoder, and constrained by a per-chunk permission filter.

## 1. Requirements

### 1.1 Functional requirements

- Ingest documents. Accept a document, then chunk, embed, and index it asynchronously.

- Answer queries. Return the top-k chunks for a question, with their source documents for citation.

- Hybrid retrieval. Match both meaning and exact terms.

- Update and delete. A changed document is re-indexed; a deleted one disappears from results.

- Tenant-scoped retrieval. Every result belongs to the asker's tenant and passes their ACL.

### 1.2 Non-functional requirements

- Low retrieval latency: tens of milliseconds at p99, since generation dominates the total answer time.

- High recall: the right chunks must be among those returned; a missing chunk produces a wrong or unsupported answer.

- Freshness: changes visible within minutes, deletes immediately.

- Strict tenant isolation: a query never returns another tenant's chunk or a chunk the user cannot read.

- Scale: on the order of billions of chunks.

- Graceful degradation: slightly stale or slightly fewer results are better than an error.

### 1.3 The constraint versus the property

The binding constraint is memory: billions of vectors must sit where an ANN index can search them in milliseconds. The non-negotiable property is isolation: a fast index that leaks another tenant's chunk is wrong. The design repeatedly trades index efficiency against the cost of filtering correctly.

Key idea. Memory bounds what the index can hold; isolation bounds how it may be shared.

## 2. Back-of-the-envelope estimation

The defaults below are illustrative assumptions: 100M documents, about 10 chunks each, 768-dimension float32 embeddings, 10,000 queries per second, about 1,000 chunks per second of embedding throughput per GPU, and 1% of documents changing each day.

Documents100M

Chunks per document10

Embedding dimensions768

Vector precisionfloat32 (4 B/dim)float16 (2 B/dim)int8 (1 B/dim)

Query QPS10.0K

Embed rate per GPU (chunks/s)1.0K

Daily document churn1.0%

Vectors to index

1.0B

documents × chunks per document

Raw vector memory

3.1 TB

before ANN graph links or replicas

Document text (10 KB each)

1.0 TB

cheap object storage

Brute-force comparisons/s

10.0T

vectors × QPS: why ANN is required

Initial backfill

278 GPU-h

1.0M GPU-seconds

Daily re-embed

10.0M chunks

2.8 GPU-hours per day

All outputs are derived from the inputs above. The defaults are illustrative assumptions, not measurements.

### 2.1 Index size

100M documents × 10 chunks ≈ 1B vectors. At 768 dimensions × 4 bytes ≈ 3 KB per vector, raw vectors take about 3 TB, before HNSW links or replicas. The document text, at roughly 10 KB per document, is about 1 TB, and it lives on cheap object storage. The vectors are the expensive part because the index wants them in RAM.

### 2.2 Query load

Brute force at 10,000 QPS against 1B vectors is 10^9 × 10^4 = 10^13 distance computations per second, each over 768 dimensions. No reasonable fleet does that. ANN search is required, not an optimization.

### 2.3 Ingestion

The initial backfill embeds 1B chunks. At 1,000 chunks per second per GPU, that is 10^6 GPU-seconds, about 280 GPU-hours, a one-time job spread across many GPUs. Daily churn of 1% is 1M documents, or about 10M chunks per day, roughly 3 GPU-hours of embedding. Steady-state ingest is modest; the backfill and any model change are the large jobs.

Key idea. Memory for about 3 TB of raw vectors, not compute or document bytes, is the number that shapes the design.

## 3. API design

Design checkpoint

Embedding and indexing a document takes seconds to minutes. What should POST /documents return?

Block until the document is searchable, then return 200Return immediately with an indexing status the client can poll

The calls follow the data: documents enter, become searchable, can be removed, and are queried. Tenant and principal (the user or service identity) come from the authenticated session, not the request body.

### 3.1 Ingest a document

POST/v1/documents

Request & response

### 3.2 Check indexing status

GET/v1/documents/{doc_id}

Request & response

### 3.3 Delete a document

DELETE/v1/documents/{doc_id}

Request & response

### 3.4 Query

POST/v1/query

Request & response

k bounds how many chunks reach the prompt, and so bounds prompt tokens. doc_id and source let the generator cite where each claim came from.

Key idea. Ingest is asynchronous with a status contract; query returns sourced chunks scoped by the session's identity.

## 4. Data model

### 4.1 The document

Start with the document. It is the source of truth: its metadata row lives in a database and its text on object storage. Everything else in this system is derived from it and can be rebuilt.

### 4.2 The chunk

A document cannot be retrieved in pieces, and a filter cannot be applied mid-search if the tenant and ACL live only on the document row. So the chunk is its own entity, and the tenant and ACL are denormalized (copied) onto it so the index can filter without a join.

### 4.3 The index entries

The chunk's vector and its terms live in two derived indexes: the ANN vector index (embedding plus filterable metadata) and the keyword inverted index. Both are sharded the same way so a chunk's two entries sit together.

### 4.4 Where each entity lives

Document metadata goes in a relational database; document text on object storage. Chunks are partitioned by tenant. Vectors live in a sharded ANN index held in memory or memory-mapped from SSD. Keyword postings live in a sharded inverted index. Only the documents need backups, since the rest is rebuildable.

Key idea. Documents are the truth; chunks and both indexes are derived, denormalized for filtering, and rebuildable.

## 5. High-level design

Build from the simplest design and let each failure introduce the next component.

Reading the diagrams. Each step marks the components newly added at that step with a dashed outline and a NEW badge.

### 5.1 Embed and scan at query time

The simplest version stores documents and does everything per query: load the tenant's chunks, embed the question, compare it with every chunk vector, and return the closest.

This breaks twice. If chunks are embedded on the read path, each query re-embeds the corpus. Even with stored vectors, a scan over 1B vectors at 10,000 QPS is the 10^13 comparisons per second from the estimate.

### 5.2 Fix 1: ingest offline

Move chunking and embedding off the read path. A document write lands in the document store and puts an event on a message queue. Ingestion workers chunk, embed, and upsert the vectors. The query path now embeds only the question.

The scan still compares against every vector.

### 5.3 Fix 2: an ANN index, sharded

Replace the scan with an ANN index. At about 3 TB of vectors plus graph links, no single machine holds it, so the index is split into shards (see partitioning). A query fans out to every shard, each returns its local top-k, and the query service merges them — scatter-gather. Replicas of each shard absorb load and stragglers.

Now search is fast, but a question about E1042 returns chunks about similar errors instead of the one runbook that names it.

### 5.4 Fix 3: add keyword search and fusion

Add a keyword index beside the vector index, written by the same ingestion workers. The query runs both searches and fuses the two ranked lists into one.

Fusion favors recall, so the fused list holds the right chunks but in a rough order. Sending all of it to the model raises cost and latency, and irrelevant chunks distract the model.

### 5.5 Fix 4: re-rank with a cross-encoder

Take the top few dozen fused candidates and score each one with a cross-encoder. Keep the top handful. This is a two-stage funnel: cheap and wide first, then expensive and narrow.

Results are now relevant, but nothing yet stops a user at tenant acme from receiving a chunk that belongs to tenant globex.

### 5.6 Fix 5: filter by tenant and ACL in both indexes

Every index entry carries tenant_id and acl_tags. The query service derives the tenant and principal from the session and passes them as a filter to both searches, so a disallowed chunk is never a candidate. Large tenants get dedicated index partitions; small tenants share one with filtering. The deep dive on the ANN index explains why the filter must run inside the search.

### 5.7 Fix 6: keep the indexes fresh

A document edit must be retrievable within minutes, and a delete must vanish now. Ingestion re-embeds only changed chunks (compared by content hash). A delete writes a tombstone — a marker that masks the chunk at query time — before the index entries are physically removed later. The freshness deep dive covers how an ANN graph absorbs changes.

### 5.8 The query flow

### 5.9 The composed design

Key idea. Ingest offline, search a sharded filtered ANN index plus a keyword index, fuse, re-rank, and hand a short sourced list to generation.

## 6. Deep dives

### 6.1 The ANN index

Before reading on, consider: with 3 TB of vectors, which index do you pick, and how do you know it still finds the right chunks next month?

The index is a three-way budget among recall, latency, and memory. HNSW gives high recall at low latency but stores every full vector plus its graph links, so it is memory-hungry. IVF-PQ combines two ideas. The inverted file (IVF) clusters vectors and, at query time, searches only the few clusters nearest the query. Product quantization (PQ) compresses each vector: it splits the 768 numbers into, say, 96 sub-vectors of 8 numbers, replaces each sub-vector with the id of its closest entry in a small learned codebook of 256 entries, and so stores 96 one-byte codes instead of 3 KB. Memory drops sharply; distances become approximate, and recall drops some. A design picks two of the three and pays for the third.

Sharding uses scatter-gather with a top-k merge. With many shards, one slow shard sets the latency, so each shard has replicas and the query service sends to the fastest. Past a deadline, it returns a partial merge from the shards that answered. Fewer candidates beat an error, and the partial-result rate becomes a metric.

Filtering is the hard part. The widget compares two orders of operations.

Search, then filterFilter during traversal

Tenant's share of index:

50%20%5%

▶ Run query (k = 5)Reset

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

Candidates examined

0

Permitted results returned

0 / 5

Squares are candidates in order of distance to the query. Green = the querying tenant's chunk, red = another tenant's chunk (discarded). “Search, then filter” fetches a fixed 10 candidates and filters afterward; “filter during traversal” keeps walking until it holds 5 permitted chunks.

Design checkpoint

A small tenant owns 1% of a shared index. A query asks for k = 5. What happens if the index finds the 10 nearest chunks and then drops other tenants' chunks?

It returns 5 permitted chunks, slightly slowerIt often returns zero or very few chunks, because most of the nearest 10 belong to other tenants

Post-filtering (search, then drop disallowed chunks) returns too few results when the tenant is a small slice of the index. Pre-filtering (select allowed chunks, then search only them) loses the index and becomes a brute-force scan. Production systems combine three remedies. Large tenants get their own per-tenant index, so no filtering is needed. Small tenants share an index whose traversal checks the filter during the walk, skipping disallowed nodes but continuing until it holds k permitted results. When a filter is very selective, for example a single user's private folder, the matching set is small enough that an exact scan over it is cheaper than any graph walk.

The hidden failure is silent recall decay. A bad rebuild, a parameter change, or a new filter can drop recall without raising an error; answers just get worse. Monitor recall on a fixed query set with known exact neighbors, per-shard p99 latency, the partial-result rate, and recall for filtered queries specifically.

What separates answers — the ANN index

BadBrute force, or 'a vector database handles it'▾

GoodNames HNSW vs IVF-PQ and shards with scatter-gather▾

GreatPer-tenant plus in-traversal filtering plus exact fallback, with recall monitored▾

### 6.2 Retrieval quality

Before reading on, consider: the index finds the nearest vectors quickly. Why can the answer still be wrong?

Nearest is not the same as relevant. Quality depends on four choices. The first is chunking. Chunks that are too large blur several topics into one vector; chunks that are too small lose the context needed to answer. Moderate, structure-aware chunks with some overlap and the section header preserved are the usual start, and the size is tuned against a measured metric rather than guessed.

The second is hybrid retrieval. Vector search covers meaning; BM25 covers names and identifiers. The two produce scores on different scales, so they are combined by rank, not score, using reciprocal-rank fusion (RRF): each chunk scores Σ 1/(60 + rank) across the lists it appears in. A chunk ranked well in both lists rises. The widget runs the fusion on two lists and then re-ranks.

Query: payment fails with error E1042

▶ Fuse and re-rankStepReset

Vector search (meaning)

1. c3 payment retries

2. c7 checkout failures

3. c1 E1042 runbook

4. c9 billing FAQ

5. c4 refund flow

Keyword search (exact terms)

1. c1 E1042 runbook

2. c5 E1042 changelog

3. c7 checkout failures

4. c8 error code table

5. c3 payment retries

Reciprocal-rank fusion: Σ 1/(60 + rank)

Press play to score each chunk.

A chunk found by both retrievers collects two fusion terms and rises. Cross-encoder scores are illustrative.

The third is re-ranking. Fusion is tuned for recall, so its top few dozen probably contain the answer. A cross-encoder scores those few dozen and keeps a handful. The fourth is how many chunks to send. More chunks raise time-to-first-token and cost, and irrelevant chunks distract the model, so the system sends few, high-relevance chunks.

Design checkpoint

A team changes the chunk size. How should it decide whether the change helped?

Read a few answers and judge whether they look betterMeasure recall@k and rank quality on a fixed set of queries with known relevant chunks

Evaluation closes the loop. An offline set of queries with known-relevant chunks measures recall@k and rank quality for every change to chunking, models, or fusion. Online, the citation rate (how often the answer cites a returned chunk) and user thumbs signals act as proxies. Returning doc_id and source with every chunk lets the answer cite its evidence, which bounds unsupported claims.

What separates answers — retrieval quality

BadVector search only, top-k straight into the prompt▾

GoodHybrid retrieval with re-ranking▾

GreatFunnel tuned and measured end to end▾

### 6.3 Freshness

Before reading on, consider: an HNSW graph is a web of links. What does it cost to insert or delete one node in place, millions of times a day?

Re-embedding everything on each change is wasteful, so ingestion re-embeds only changed documents. Within a changed document, each chunk's content hash is compared with the stored hash, and unchanged chunks are skipped. Changed chunks are upserted into both the vector and keyword indexes.

ANN graphs do not mutate cheaply in place, so the index follows the log-structured merge pattern. New and changed vectors go into a small, fresh segment that is searched alongside the main index. Deletes write tombstones, which mask the chunk at query time immediately. Periodically, a background job merges the fresh segment and drops tombstoned entries into a rebuilt main index. The merge schedule trades freshness against rebuild cost.

Design checkpoint

The team upgrades to a better embedding model. What happens to the existing 1B vectors?

Re-embed documents gradually and mix old and new vectors in one indexBuild a shadow index with the new model, then swap to it atomically

A new embedding model invalidates every vector, because vectors from two models are not comparable. The system builds a shadow index with the new model alongside the live one, re-embedding the full corpus (the backfill-sized job from the estimate), validates its recall, and then swaps traffic to it atomically.

The failures here are quiet. If ingestion falls behind, results go stale without any error. Monitor indexing lag (time from document write to indexed), the dead-letter rate of failed re-embeds, and any tombstoned chunk still being returned. A dead shard degrades to fewer candidates and is rebuilt from the document store, which is the source of truth.

What separates answers — freshness

BadRebuild the index nightly▾

GoodIncremental re-embed with tombstoned deletes▾

GreatFresh segment + merge, shadow index for model changes, lag monitored▾

Key idea. The index trades recall for memory, quality comes from a measured funnel, and freshness comes from small segments plus tombstones merged in the background.

## 7. Variants

### 7.1 10× scale

At 10B chunks, quantize harder, shard finer, and tier the index: hot tenants in memory, cold tenants memory-mapped from SSD. Scale query throughput with read-only replicas of each shard.

### 7.2 Per-tenant versus shared index

Large tenants get dedicated indexes; small tenants share one with filtered traversal. Many systems run both, with a threshold on tenant size deciding which side a tenant lives on.

### 7.3 Structured filters

Filters on date, document type, or author extend the same filtered-search problem. Each selective predicate risks the same too-few-results failure, so the same remedies apply.

### 7.4 Multimodal corpora

Images, audio, and code use a different embedder, but the pipeline — chunk, embed, index, fuse, re-rank — stays the same.

Key idea. At larger scale the same design survives by compressing, tiering, and splitting tenants by size.

## 8. The transferable pattern

RAG retrieval is a search system with three reusable parts. An offline pipeline turns source records into derived, rebuildable indexes. A funnel retrieves wide and cheap, then narrows with an expensive scorer. A permission predicate travels with every derived record, so filtering happens inside the search rather than after it. The same shape fits product search, code search, and any per-tenant recommendation system.

Key idea. Derive indexes offline, funnel from cheap to expensive, and carry permissions on every derived record.

## Review

- Ingest offline: chunk documents, embed chunks, and index the vectors before queries arrive.

- Retrieve with an ANN index (HNSW or IVF-PQ), sharded with scatter-gather.

- Go hybrid: vector and keyword search, fused by rank, then a cross-encoder re-ranker.

- Stay fresh with incremental re-embedding and tombstoned deletes; filter every chunk by tenant and ACL.

- Pass a few top chunks, with sources, to the generation tier.

## Quiz

RAG System Design Quiz

Hide AllReveal All

1)Why can't a RAG system put the whole corpus into the model's prompt?

2)What dominates the infrastructure cost of the index, and why?

3)Why does filtering after an ANN search fail for a small tenant in a shared index?

4)Why fuse vector and keyword results by rank instead of by score?

5)Why use a cross-encoder only on a short list?

6)How does a delete become invisible immediately when the ANN graph cannot be changed cheaply?

7)What must happen when the embedding model changes?

## Sources and further reading

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — Lewis et al., 2020 — the paper that named and defined RAG.

- Efficient and robust approximate nearest neighbor search using HNSW graphs — Malkov and Yashunin — the HNSW index and its layered greedy search.

- Product Quantization for Nearest Neighbor Search — Jégou, Douze, Schmid — product quantization and the IVF-ADC index behind IVF-PQ.

- The Faiss library — Douze et al., 2024 — the recall, latency, and memory trade-offs across ANN index types.

- Reciprocal Rank Fusion outperforms Condorcet and individual rank learning methods — Cormack, Clarke, Büttcher — the RRF formula and its constant of 60.

- The Probabilistic Relevance Framework: BM25 and Beyond — Robertson and Zaragoza — the BM25 keyword-scoring function.

- Sentence-BERT — Reimers and Gurevych, 2019 — bi-encoder versus cross-encoder trade-offs.
