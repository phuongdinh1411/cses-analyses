---
layout: simple
title: "Search Engines & Inverted Index — System Design School"
permalink: /system_design/sds/concepts/domain-search
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

Distributed Systems

Search, Feeds & Spatial

Search Engine Mechanics

- Inverted Index Fundamentals

- TF-IDF Scoring Explained

- BM25 and Parameter Tuning

- Elasticsearch Architecture Essentials

- Advanced Search Patterns

Feeds & Ranking

- Two-Stage Ranking

Geospatial Search

- Geospatial Search Introduction

- Geohash

- QuadTrees

- H3 Hexagonal Hierarchical Spatial Index

- Space-Filling Curves and Hilbert’s Curve

- Google's S2 Library

- Designing a Map Rendering Service

- Choosing a Spatial Index

Specialized Systems & Data Structures

# Inverted Index Fundamentals

Start quizSave

Searching for a phrase across millions of documents with a full scan requires reading every document from start to finish. A SQL LIKE '%wireless%' query cannot use a standard B-tree index because the leading wildcard prevents prefix lookup, so the database inspects every row. An inverted index flips that layout: instead of mapping each document to the words inside it, it maps each unique term to the sorted list of documents that contain that term.

## Core Structure of an Inverted Index

An inverted index separates search into two structures: a term dictionary and a set of posting lists.

- Term dictionary: an alphabetically sorted table (or finite-state transducer) of every unique normalized term in the corpus, pointing to its posting list on disk or in memory.

- Posting list: for a single term, an ordered list of postings sorted by ascending document ID (docID). Each posting stores the docID and optional metadata such as term frequency (how many times the term appears in that document) and word positions (where it appears, needed for phrase queries).

Because postings are stored in ascending docID order, the engine can compress them with delta encoding (storing the gap between consecutive IDs rather than full integers) and intersect multiple lists in a single linear pass.

## Text Analysis: Tokenization, Normalization, and Stemming

Raw text rarely matches user queries character for character. A catalog entry "Wireless Headphones with noise cancelling" and a query "wireless headphone" differ in capitalization, punctuation, and plural suffix. Before inserting terms into the dictionary, the engine passes every document through an analyzer pipeline.

- Tokenization: split raw text on whitespace and punctuation into individual tokens, recording each token's ordinal position.

- Case folding (lowercasing): convert every token to lowercase so "Wireless" and "wireless" map to the same dictionary key.

- Stop-word handling: optionally drop high-frequency function words ("and", "for", "with") while keeping token positions intact so phrase adjacency stays accurate. Modern engines often retain stop words in the index and rely on ranking formulas to down-weight them, because dropping them prevents exact phrase queries like "to be or not to be".

- Stemming or lemmatization: reduce inflected forms to a shared root so "headphones" and "headphone" both index under "headphone". A stemmer applies heuristic suffix rules (fast, occasional over-stemming), while a lemmatizer uses a vocabulary dictionary to produce valid base words.

The engine must run the exact same analyzer on incoming queries as it ran during indexing. If documents are lowercased and stemmed at index time, a query that skips stemming will look up "headphones" in a dictionary that only contains "headphone" and miss every matching document.

Press Play in the widget below to watch the analyzer index a 5-product catalog step by step and then compare a SQL LIKE scan against an inverted index lookup for "wireless headphones". Then select "wireless headphones" (phrase) or phone to see how positions and tokenization change the result.

Step: tokenize product 1PlayReset

Querywireless headphones"wireless headphones"phonewired OR sport

The catalog has 5 products and the index is empty. Press "Step: tokenize product 1" to start indexing, or press Play to index all 5 products and then run the query "wireless headphones".

Catalog (rows in the products table)

1

Over-ear wireless headphones

2

Studio headphones, wired

3

Wireless charger for phones

4

Wireless Headphones with noise cancelling

5

Sport headphone, wireless and sweatproof

Inverted index: 0 terms, 0 postings

Empty. Index a product to add its terms.

Each entry is a product ID with its word positions in [ ]. The term frequency is the number of positions.

LIKE is case-sensitive here, as in PostgreSQL. The stemmer in this widget only removes a plural "s"; real stemmers do more. With 10 million products, the scan reads 10 million rows, while the engine still reads only the lists of the query terms.

## Boolean Intersection and Skip Pointers

When a user enters a multi-term query such as wireless AND headphone, the engine looks up each term in the dictionary, retrieves its sorted posting list, and intersects them with a two-pointer merge.

Both pointers start at the beginning of their respective posting lists:

- If both pointers reference the same docID, the engine records a match and advances both pointers.

- If one pointer references a smaller docID, the engine advances that pointer because neither list can contain that smaller ID later.

For lists of length m and n, a plain two-pointer merge inspects at most m + n entries. When one list is very long (a common term like "wireless") and the other is short (a rarer term like "headphone"), stepping one entry at a time through the long list wastes comparisons.

Search engines add skip pointers to long posting lists. A skip pointer is a shortcut stored at regular intervals along a posting list that jumps directly to a later docID and its byte offset. A classic textbook heuristic places skip pointers every √L entries for a list of length L, balancing jump distance against the extra storage and comparison overhead. During intersection, if the current docID in the longer list is smaller than the target docID in the shorter list, the engine checks the skip target. When the skip target is still less than or equal to the target docID, the pointer jumps straight across the intermediate postings without decoding them.

In the diagram above, intersecting wireless ([d2, d5, d9, d14, d18, d23, d31]) with headphone ([d18, d31, d40]) starts at d2 and d18. Because d2 < d18 and the skip target d18 is less than or equal to d18, the pointer jumps directly from d2 to d18, bypassing d5, d9, and d14. For queries with three or more AND terms, the engine intersects the shortest posting lists first, shrinking the candidate set before touching longer lists.

For an OR query (union), the engine walks the lists with the same sorted pointers and emits every unique docID encountered in ascending order. For a phrase query ("wireless headphones"), the engine first intersects the docID lists and then checks the stored word positions to confirm that "headphone" appears immediately after "wireless".

## Time and Space Complexity

Suppose a corpus holds N documents with an average of M words each, and a query has k terms whose posting lists contain p total postings examined.

- Full scan: inspects every word of every document, taking O(N × M) work. On a corpus of 1,000,000 documents averaging 500 words each, a full scan reads 500,000,000 words.

- Inverted index lookup: looks up k terms in the dictionary and merges p postings, taking O(k + p) work (reduced further by skip pointers when one list is much shorter than another).

In memory and on disk, the dictionary stores each unique term once regardless of how many times it appears across the corpus, and delta-compressed posting lists store compact integer offsets rather than raw text.

## Hands-On Implementation

The two code editors below show a minimal inverted index and a standalone text preprocessing pipeline in Python.

#### Basic Inverted Index Implementation

Inspect how documents are tokenized into posting sets and intersected for multi-term queries

Loading...

Loading Python environment... This may take a few seconds on first load.

#### Text Preprocessing for Search

Trace lowercasing, punctuation removal, tokenization, and stop-word filtering

Loading...

Loading Python environment... This may take a few seconds on first load.

## Production Trade-Offs

An inverted index makes reads fast at the cost of extra write work and storage overhead.

- Write amplification and immutability: updating a single posting list in place on disk requires shifting bytes. Production search engines such as Apache Lucene avoid in-place edits by buffering writes in memory and flushing immutable index segments, which are later merged in the background (covered in Elasticsearch Architecture Essentials).

- Index size: storing term positions for phrase queries and payloads for scoring increases disk footprint compared to storing docIDs alone. Teams disable position indexing on fields that only need exact or boolean matching.

- Unranked results: boolean intersection determines which documents match, not which matching document is most relevant. When a query matches thousands of documents, the engine needs a relevance scoring function such as TF-IDF or BM25, covered in the next two lessons.

Explain

Add to Chat

Start QuizLoading

Send feedback
