---
layout: simple
title: "Tries & Prefix Search — System Design School"
permalink: /system_design/sds/concepts/tech-tries
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

Networking EssentialsTechnology ChoicesRedisTries & Prefix SearchFail-Open vs Fail-Closed

# Tries and Prefix Search: How Autocomplete Works

mediumAutocompleteTriesSearch

Autocomplete has to answer on every keystroke. Typing "car" should surface the top completions — "cardinals," "car rental," "cardi b" — in a few milliseconds, ranked by popularity, from a corpus of 10 million terms. The load is one query per keystroke per user, so "c," then "ca," then "car" each fire separately.

A relational database cannot hold that path. SELECT term FROM terms WHERE term LIKE 'car%' ORDER BY popularity LIMIT 5 range-scans, sorts the matches, and returns. On 10 million rows at keystroke rate, that is far too slow and far too much load. Prefix lookup needs a structure built for exactly this shape.

## The trie structure

A trie (prefix tree) stores strings as a character-keyed tree. Each edge is labeled with one character. Each path from the root spells a prefix. A node is marked as a word end when the path to it forms a complete term.

Consider three words: "cat," "car," and "card." They share the prefix "ca." The trie stores that prefix once. From the root, edge c leads to a node, then a, then the path forks: t completes "cat," while r completes "car" and also continues to d for "card." The shared prefix "ca" is a single path, not three copies.

Lookup walks the tree one character at a time. To find completions for "ca," start at the root, follow edge c, then edge a, and stop. Everything in the subtree below that node is a valid completion. The walk took two steps because the prefix has two characters.

That cost is the reason tries fit autocomplete. Lookup is O(prefix length): the work depends only on how many characters were typed, not on how many terms exist. A 10-million-term corpus and a 10-thousand-term corpus both resolve a 3-character prefix in three steps. Corpus size does not enter the equation.

Trie vs hash map. A hash map finds an exact key in one step, but it cannot answer "all keys starting with car." Its keys are scattered by the hash, so prefixes carry no locality. A trie groups every term under its prefix by construction, which is exactly what autocomplete needs.

## Autocomplete is a trie plus precomputed top-K

Reaching the "ca" node gives every completion below it. But a search box shows five suggestions, not five thousand, and it shows the popular ones first. The trie finds matches; it does not rank them. Ranking every match on each keystroke would drag the expensive work back onto the request path.

Store the answer instead of computing it. At every node, keep a small sorted list of the K most popular completions in its subtree. The "ca" node holds [cardinals, car rental, cat videos, cardi b, cargo], already ordered by popularity. A request walks to the node and returns its list. No ranking happens at request time.

The ranking work moves offline into a batch job. Aggregate the query logs to count how often each term is searched. Build the trie from those counts, and as the build walks each subtree, record the top K terms at every node, sorted. Load the finished trie into memory and serve reads from it. Rerun the batch job on a schedule, hourly or daily, to refresh popularity as search trends shift.

This inversion is the whole design. Expensive preprocessing runs once per rebuild; the request path becomes a cached lookup. The structure is read-heavy, held in memory, and built in batch. Writes do not touch it live; they land in the logs the next rebuild consumes.

The cost is staleness. A term that starts trending after the last rebuild will not appear until the next one. For autocomplete that is acceptable: a suggestion list a few hours behind still helps the user, and a small real-time layer can patch in very recent trends while the bulk stays precomputed. The Typeahead solution works this trade through end to end.

## Radix compression for memory

A naive trie spends one node per character. Long words with no branching become long chains of single-child nodes, each with its own object and pointers. On a real vocabulary that overhead is large.

A radix tree (also called a Patricia trie) collapses each chain of single-child nodes into one edge labeled with the whole substring. Where a plain trie stores "card" as c→a→r→d (four nodes past the root), a radix tree stores it as a single edge card when nothing branches off those characters. The edge splits only when a second word forces a fork.

Compression keeps the same O(prefix length) lookup while cutting node count sharply on sparse branches. The tradeoff is a slightly more complex walk: matching a prefix now compares against substrings on edges, not single characters, and inserting a word can split an edge in two. For a read-heavy structure built in batch, that extra build-time work is a good trade for the memory saved.

## Scaling the prefix layer

A single machine holds only so much trie. Beyond that, split the corpus across shards. The natural key is the prefix itself: route a* terms to one shard, b* to another, and so on. Each query names its own shard from the first characters typed, so a lookup touches exactly one shard rather than fanning out.

The catch is skew. Letters are not evenly used. Far more English terms start with s or t than with z or q, so a one-letter-per-shard split leaves some shards overloaded and others idle. Balance by splitting hot prefixes finer: give s its own group of shards keyed on the second character (sa*, sc*, st*), while rare letters share one shard. This is prefix-aware partitioning; the Database Partitioning fundamentals cover the general skew problem.

Short hot prefixes add a second pressure. Single characters like a and two-letter prefixes like th are queried constantly, since every longer query passes through them. Front the prefix layer with a cache holding the top-K lists for the most common short prefixes. Those requests never reach a shard. Because the top-K lists are small, immutable between rebuilds, and read constantly, they are close to an ideal cache entry — see the caching mental model for when this fit holds.

Design checkpoint

Autocomplete must return ranked suggestions on every keystroke, within a few milliseconds. Where should the ranking happen?

At request time, sorting matches by popularity per keystrokeOffline in a batch job, storing the sorted top-K at each nodeIn the database, with an ORDER BY popularity query

## What a strong answer sounds like

Design autocomplete for a search box over 10M terms.

BadQuery the database per keystroke▾

GoodUse a trie for prefix lookup▾

GreatTrie plus precomputed top-K, sharded and cached▾

## The transferable pattern

Autocomplete shows a general move: when reads must be fast and ranking is expensive, precompute the ranked answer offline and serve it as a cached lookup. The request path does no work beyond finding the right precomputed list. Writes flow into logs that a batch job consumes on a schedule, and the system accepts bounded staleness in exchange for near-constant read latency.

The same shape appears in feed generation, "related items" panels, and leaderboards: heavy ranking runs in batch, the serving layer reads a small precomputed result. Prefix search adds one specialization — the trie — because the lookup key is a growing prefix, and no hash or B-tree groups terms by shared prefix the way a character-keyed tree does.

Key idea. Autocomplete is a trie for prefix lookup plus a precomputed top-K list at each node, so ranking happens once in batch and the keystroke path is a cached read.

## Sources and further reading

- Trie — Wikipedia — the prefix-tree structure and O(prefix length) lookup.

- Radix tree — Wikipedia — how single-child chains compress into labeled edges.

- Completion Suggester — Elasticsearch docs — a production prefix-completion suggester built on an in-memory FST, precomputed at index time.

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

The trie structureAutocomplete is a trie plus precomputed top-KRadix compression for memoryScaling the prefix layerWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageThe trie structure0%

Send feedback
