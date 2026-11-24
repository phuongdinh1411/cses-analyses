---
layout: simple
title: "Design Deep Research Agent — System Design School"
permalink: /system_design/sds/deep-research
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

RAG SystemChatGPTImage Generation ServiceCoding Agent CLI (Claude Code)Deep ResearchReasoning Effort Levels

Patterns5

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time Transport

Show all 5 →

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# Design Deep Research

hardAI agentsAsync processingContext managementCachingCheckpointing

Practice this problem

ScopeHLDE2EScalingCapacity

## Problem statement

Design a deep-research feature on top of a chat assistant. A user asks one hard question, such as "How do the leading solid-state battery designs compare on cost and cycle life?" The system plans an investigation, runs many web searches, and reads dozens of sources. After several minutes and many model and tool calls, it returns a long report with citations.

In scope: accepting the question, planning, searching and fetching sources, reading and compressing them, synthesizing a cited report, and streaming progress to the user. Out of scope: the model-serving layer itself (batching, token streaming, GPU scheduling) and the web crawler's fetch and politeness logic. Both are treated as existing services this design calls.

## Clarifying questions

Each question below comes with the assumption its answer sets:

- What does the user get back? One question in, one cited report out, delivered asynchronously. Steering the job while it runs is a variant.

- Where do sources come from? The open web, through a search API and an existing fetch layer that already respects per-site rate limits (politeness). A private document corpus is a variant.

- What limits a job? An effort budget: a cap on tokens, wall-clock time, and number of searches, chosen per job.

- How do we size it? By tokens per job, sources per job, and minutes per job, not requests per second. A few thousand concurrent jobs is a small request rate but a large token bill.

- Is model serving in scope? No. The design calls an inference API for generate, summarize, and synthesize steps.

Token. The unit a language model reads and writes, roughly three-quarters of an English word. Model cost and the context-window limit are both measured in tokens.

## What makes this problem distinctive

A chat turn is one request and one response. A research job is the opposite shape: one request that turns into hundreds of dependent model and tool calls over minutes. That changes the system from a request-serving problem into a job-orchestration problem.

Two forces pull against each other inside every job. Thoroughness wants more sources, because more sources mean better coverage and more corroboration of each claim. Budget pushes back, because every extra source costs tokens, wall-clock time, and space in the model's context window. A model can only read a fixed number of tokens at once, so the raw text of many sources cannot be pasted into one prompt.

A third constraint sits under both: the report must be grounded. Every claim must trace back to a source the job actually read. A fluent report with an invented citation is a failure, even if it reads well.

Key idea. Deep research is a long job, not a request, and its core tension is thoroughness against a fixed budget and a fixed context window.

## Key concepts

This section covers the concepts needed to solve this problem — prerequisites for the design work that follows.

### The context window

A context window is the maximum number of tokens a model can read in one call, including instructions, inputs, and its own output. Anything outside the window does not exist for that call. If a job reads 50 web pages of up to 10,000 tokens each, the raw text is 500,000 tokens. A model with a window of roughly 200,000 tokens cannot see all of it at once. The design must decide what goes into each call.

### The agent loop (ReAct)

An agent loop is a program that calls a model repeatedly and lets the model choose actions. The common form is ReAct (reason and act). The model reasons about what it knows, picks an action such as "search for X", the orchestrator runs that tool, and the result goes back to the model as an observation. The loop repeats until the model decides it has enough. The loop can be a prompt scaffold around a general model, or the behavior can be trained into the model. OpenAI describes its deep-research agent as a version of its o3 model trained with reinforcement learning on browsing tasks (source).

### Map-reduce summarization

Map-reduce summarization fits large inputs through a small window in two passes. The map pass summarizes each source on its own, so each call holds only one page. The reduce pass merges summaries into larger units, level by level, until one output remains. No single call holds all the raw text. Each summary keeps the id of the source it came from, so a citation survives every level.

PlayStep Reset

1. Raw sources2. Map: summaries3. Reduce: findings4. Reduce: sections5. Report

Context window use: 120,000 / 50,000 tokens

Concatenating raw pages overflows the window.

Illustrative sizes: 12 sources, 10K raw tokens each, a 50K-token window.

Step through the phases. The raw pages overflow the window. After the map pass, the same 12 sources fit with room to spare, and each reduce level shrinks the input again.

### Checkpointing

A checkpoint is a saved copy of a job's progress in durable storage. If the worker running the job crashes, a new worker loads the latest checkpoint and continues from there instead of from the beginning. For a job made of hundreds of paid model calls, the difference between "resume" and "restart" is real money and minutes of user wait.

### Grounding

Grounding means each claim in the output is backed by a specific retrieved source. A model can write fluent text that no source supports; this is called a hallucination. A grounded pipeline makes that hard by construction: the synthesis step only receives retrieved summaries, each tagged with a source id, and it must cite those ids.

Key idea. The window limits what one call can see; map-reduce compresses sources to fit, checkpoints make a long job survivable, and source ids carried through every level keep the report grounded.

## 1. Requirements

Practice this problem: Requirements

Before reading on. List the functional and non-functional requirements. Then name the one property you will not trade away and the one constraint that shapes the design.

### 1.1 Functional requirements

The verbs in the problem statement give the requirements:

- Submit a question with an effort level, and receive the report asynchronously.

- Plan by splitting the question into ordered sub-questions.

- Retrieve sources through search, fetch, and text extraction; then read, compress, and run follow-up searches to fill gaps.

- Synthesize a cited report and stream progress while the job runs.

The search API, the fetch layer, and model serving are existing dependencies. This design calls them and owns everything between.

### 1.2 Non-functional requirements

- Groundedness. Every claim traces to a cited source.

- Budget-bounded cost. Hard caps on tokens, wall-clock time, and searches per job.

- Visible progress. Status updates stream to the user, so a five-minute job never looks hung.

- Reliability. A job resumes from checkpoints after a worker failure, and returns partial results if it cannot finish.

- Scale. Many concurrent jobs, each running for minutes.

### 1.3 The constraint versus the property

Groundedness is the non-negotiable property. A shorter report is acceptable; an uncited claim is not. The budget is the constraint that drives the design. It forces compression, caching, parallelism, and a stop rule. The two collide at one decision: how many sources to gather and how hard to compress them.

Key idea. Protect groundedness; design around the budget; the collision point is how many sources to read and how much to compress them.

## 2. Back-of-the-envelope estimation

Practice this problem: Back-of-the-envelope estimation

A research job is sized in tokens, not requests. The calculator uses the illustrative inputs below; move the sliders to see when the raw text and the summaries stop fitting in one window.

Sub-questions per job10

Sources read per sub-question5

Raw tokens per source (up to)10K

Summary tokens per source500

Model context window200K

Sources per job

50

10 × 5

Raw source tokens

500K

exceeds the window

After map (summaries)

25K

fits the window

Compression ratio

20×

raw ÷ summaries

Illustrative inputs. The window check ignores instructions and output tokens, so the real headroom is smaller.

### 2.1 Tokens per job

Assume a chat turn uses on the order of 1,000 tokens. A research job runs planning, dozens of searches, a summary per source, several reduce levels, and a long final report. A reasonable working figure is on the order of 1,000,000 tokens per job, roughly a thousand chat turns' worth. Tokens per job, not job count, drives cost.

### 2.2 Sources and the window

Assume 10 sub-questions with 5 sources each: 50 source reads per job. At up to 10,000 tokens per page, raw text is 500,000 tokens. That exceeds a window of roughly 200,000 tokens. If each source is summarized to about 500 tokens, the 50 summaries total 25,000 tokens, a 20× reduction that fits comfortably with room for instructions and output.

### 2.3 Wall-clock time

With sequential model calls and page fetches, a job takes on the order of 5 minutes. No user holds an HTTP request open that long, and no load balancer should either. The job must run asynchronously, with its progress streamed separately.

Key idea. The binding numbers are about a million tokens and minutes of wall-clock per job; raw sources overflow the window by more than 2×, and per-source summaries shrink them about 20×.

## 3. API design

Practice this problem: API design

Design checkpoint

A job takes about five minutes. How should the client submit a question and get the report?

POST the question and hold the request open until the report is readyPOST returns a job id immediately; the client follows progress on a stream and fetches the report when done

The calls follow the life of a job: submit it, watch it, stop it, read the result. The user comes from the authenticated session, never from the request body.

### 3.1 Submit a question

The server stores the job, enqueues it, and returns 202 Accepted at once. The effort value maps to a budget preset.

POST/v1/research

Request & response

### 3.2 Read status

GET/v1/research/{job_id}

Request & response

### 3.3 Stream progress

Server-Sent Events (SSE) is a one-way HTTP stream where the server pushes text events to the browser over a long-lived response. Event types here are plan, step, source_found, partial, and done. Each event carries an id, so a reconnecting client sends Last-Event-ID and resumes the stream without gaps.

GET/v1/research/{job_id}/stream

Request & response

### 3.4 Cancel

Cancel stops the loop and releases the remaining budget. Work already checkpointed stays readable.

POST/v1/research/{job_id}/cancel

Request & response

### 3.5 Fetch the report

GET/v1/research/{job_id}/report

Request & response

Key idea. Submission returns a job id; the job's lifetime is separate from any connection, and progress arrives over a resumable stream.

## 4. Data model

### 4.1 The research job

Start with the job itself. It records the question, its budget, and where it is in its life.

### 4.2 The plan

A job cannot store its sub-questions or their progress, so the plan becomes its own entity. Each step has a status and a depth that counts follow-up searches.

### 4.3 The source

A plan says what to look for, not what was found. A source records one read page: its url, a reference to the fetched text in a blob store, its summary, an embedding, and a quality score. An embedding is a vector of numbers that places text with similar meaning close together; comparing two embeddings detects near-duplicate pages with different urls.

### 4.4 The finding

A summary describes one page. A claim that the report makes often rests on several pages. A finding stores one claim with the ids of every source that supports it, plus a confidence value.

### 4.5 The report and how they relate

The report holds ordered sections. Each section lists the findings it uses, and the citation list maps source ids to urls.

### 4.6 Where each entity lives

The job, plan, findings, summaries, and report live in a durable database. Together they are the checkpoint of record. The full fetched text goes to object storage or a fetch cache, referenced by fetched_ref. Embeddings go into a vector index, a store that answers "which stored vectors are closest to this one?", used here for dedup.

Key idea. Each entity exists because the previous one could not hold it; source ids link report to finding to source, which is what makes grounding checkable.

## 5. High-level design

Practice this problem: High-level design

Reading the diagrams. Components added in each step have a dashed pink outline and a NEW badge.

### 5.1 One synchronous request

The naive version handles the question inside the API request. The API server calls the model, runs searches, fetches pages, pastes them into a prompt, and returns the answer.

This breaks in three ways. The request runs for minutes, so any timeout or dropped connection loses the whole job. Pasting raw pages overflows the window, as estimation showed. And a server restart throws away every model call made so far.

### 5.2 Fix 1: run the research as a background job

Move the work off the request path. The API stores the job and puts its id on a job queue. Orchestrator workers take jobs from the queue and run the loop. The API returns at once with the job id.

For the queue's delivery semantics, see Message Queue. The job now outlives the request. But the user sees nothing for minutes, and a worker crash still loses everything.

### 5.3 Fix 2: checkpoint each step and stream progress

Add a durable store. The worker saves the plan, each source summary, and each finding as it completes. On a crash, the queue redelivers the job and a new worker resumes from the store. The same writes feed a progress stream that pushes SSE events to the user.

The job is now visible and survivable. It still pastes raw pages into one prompt, though, and overflows the window.

### 5.4 Fix 3: compress with map-reduce, store raw text separately

Split the loop's reading into a map pass and a reduce pass. The worker stores each fetched page in object storage, then asks the model to summarize that one page against its sub-question. Only the summary, tagged with its source id, enters later prompts. Reduce merges summaries into findings, findings into sections, and sections into the report.

Each page is summarized once and never re-sent raw. Two new problems appear: the same page often shows up under several sub-questions, and nothing stops a job from searching forever.

### 5.5 Fix 4: dedup and cache sources

Before reading a page, the worker checks whether this job has already seen it, first by url and then by embedding similarity in a vector index. A cross-job source and result cache stores recent search results and page summaries, so a second job asking about the same topic skips duplicate fetches and summaries. See Caching Read Patterns for the read path.

### 5.6 Fix 5: enforce an effort budget

The loop decides when it has enough, and a model can keep finding one more thing to check. Add a budget guard inside the orchestrator. Before each step it compares tokens, time, and searches spent against the job's caps. When the next step would cross a cap, the guard stops research and moves straight to synthesis with what exists.

### 5.7 The composed design

The sequence below shows one job from submission to report.

Key idea. Each component answers one failure: the queue answers request timeouts, checkpoints answer crashes, map-reduce answers the window, the cache answers duplicate spend, and the budget guard answers runaway loops.

## 6. Deep dives

Practice this problem: Deep dives

### 6.1 The agent loop and context management

Before reading on. The job has 10 sub-questions and a 200,000-token window. Decide what goes into each model call and what never does.

A planner call turns the question into ordered sub-questions. For each one, the worker searches, fetches the top results, extracts the text, and drops any page already seen by url or by embedding similarity. The loop follows ReAct: after each observation the model decides whether to search again, fetch more, or move on.

The map step summarizes each source to a few hundred tokens, written against the sub-question it serves, with the source id attached. Iterative deepening then runs follow-up searches when a summary reveals a gap or a claim needs a second source. Plan depth and budget bound how far this goes. The reduce step is hierarchical: summaries become findings, findings become sections, and sections become the report. No level holds all raw sources.

Two failure paths need explicit handling. An empty search is retried with a rewritten query, or the sub-question is marked thin. An oversized page is truncated or split into pages before summarizing. Useful metrics are sources per job, dedup rate, compression ratio, loop depth, and plan coverage when the budget runs out.

Design checkpoint

During synthesis, the model needs facts from 50 sources. What should the synthesis prompt contain?

The raw text of every source, so nothing is lostThe per-source summaries (or findings) tagged with source ids, built by earlier map and reduce steps

What separates answers — agent loop and context

BadPastes search results into one big prompt▾

GoodPlan, per-source summaries, then synthesis▾

GreatHierarchical reduce, deepening, dedup by meaning, measured coverage▾

### 6.2 Cost and latency budgeting

Before reading on. A job could run for an hour if nothing stops it. Decide what stops it, and what the user gets when it does.

The effort budget caps tokens, wall-clock time, searches, and loop depth. The orchestrator checks it before every step. It reserves enough for the final synthesis, so a stop always produces a report. When the cap arrives, it synthesizes the best report it can from what exists and lists the sub-questions it did not cover.

PlayStep ResetEffort budget: 50K tokens

Spent 0K of 50K. 10K is reserved for the final synthesis.

next · Plan: split into 4 sub-questions (6K)

skip · SQ1: search + fetch 3 pages (4K)

skip · SQ1: summarize 3 pages (map) (6K)

skip · SQ2: search + fetch 3 pages (4K)

skip · SQ2: summarize 3 pages (map) (6K)

skip · SQ2: gap found, follow-up search (5K)

skip · SQ3: search + fetch 3 pages (4K)

skip · SQ3: summarize 3 pages (map) (6K)

skip · SQ4: search + fetch 3 pages (4K)

skip · SQ4: summarize 3 pages (map) (6K)

skip · SQ4: corroborate a claim (5K)

The orchestrator checks: spent + next step + reserved synthesis ≤ budget.

Run the loop at different budgets. A small budget stops after two or three sub-questions; a larger one covers all four plus the follow-ups. In both cases the job ends with a report, not an error.

Four techniques lower cost per job without lowering coverage. Summarizing each page once keeps raw text out of every later call. Prefix caching lets the inference service reuse computation for an identical prompt prefix, such as the fixed system instructions repeated on every call. The cross-job source cache skips duplicate fetches and summaries. And independent sub-questions run in parallel, so wall-clock time tracks the slowest branch instead of the sum of all branches.

Monitor the tokens-per-job distribution (a long tail means runaway loops), cache hit rate, wall-clock p50 and p99, and the rate at which jobs hit the budget.

Design checkpoint

A job reaches its token cap with two of five sub-questions unexplored. What should it return?

An error, because the research is incompleteA shorter grounded report from what was gathered, with the gaps stated

What separates answers — budgeting

BadLets the model decide when to stop▾

GoodHard caps with graceful stop▾

GreatReserved synthesis, caching at three levels, parallel branches, tail monitoring▾

### 6.3 Reliability and grounding

Before reading on. A worker dies at minute four of a five-minute job. Then synthesis writes a claim that none of the sources support. Decide how each is caught.

Checkpoint every step: the plan, each summary, each finding. This resembles a saga, a long process split into steps with saved progress. Here the steps only read the web and write the job's own records, and each is idempotent: running it again produces the same saved result. So resuming is enough, and no compensating undo step is needed. A failed or over-budget job still returns a shorter grounded report.

PlayStep Reset

No checkpoints — steps executed: 0

planSQ1 summariesSQ2 summariesSQ3 summariesSQ4 summariesfindingssectionsreport

Checkpoint each step — steps executed: 0

planSQ1 summariesSQ2 summariesSQ3 summariesSQ4 summariesfindingssectionsreport

The worker crashes after step 5. Each step is a model or tool call, so repeated steps are repeated spend.

Play both lanes. The worker without checkpoints repeats every step after the crash. The checkpointed worker repeats none of them.

Grounding is enforced by data flow. Each finding carries source ids. The synthesis prompt contains only retrieved summaries and findings, and the model must cite ids for each claim. A verification pass then drops or flags any sentence without a supporting source. Source quality also matters: near-duplicates are merged, sources are weighted by authority, and recent sources are preferred for time-sensitive questions. When sources disagree, the report states the disagreement instead of silently picking a side.

Monitor citation coverage, resume rate, dead-source rate (cited urls that no longer load), and contradiction rate.

Design checkpoint

A resumed job re-runs the step that was in progress when the worker died. Why is that safe here?

It is not safe; the job needs compensating transactions to undo the partial stepEach step only reads the web and writes the job's own keyed record, so re-running it overwrites with an equivalent result

What separates answers — reliability and grounding

BadRetries the whole job; trusts the model's citations▾

GoodCheckpoints and source ids▾

GreatIdempotent steps, partial results, verification, quality and contradictions▾

## 7. Variants

### 7.1 10× scale

More workers and more inference capacity carry most of the load, since jobs are independent. At 10× sources per job, summaries alone pass the window (500 sources × 500 tokens = 250,000 tokens), so add another reduce level. Retrieval fan-out also grows, and per-site politeness limits in the fetch layer become the bottleneck; the cross-job cache matters more.

### 7.2 Multi-agent orchestrator-worker

A lead agent spawns several subagents, each with its own context window, for breadth-first questions. Anthropic reports that its multi-agent setup beat a single agent by 90.2% on an internal research eval, cut research time by up to 90% on complex queries, and used about 15× the tokens of a chat; token usage alone explained about 80% of performance variance in its analysis (source). The gain pays off only when the answer is worth the cost. Tasks that need tightly shared context, such as many coding tasks, often do better with one agent.

### 7.3 Private corpus

Replace web search with vector search over internal documents. Groundedness matters more, because outputs are often audited.

### 7.4 Conversational refinement

Keep the plan and gathered sources, add sub-questions from the user's follow-up, and re-run synthesis. Checkpointed state makes this cheap.

Key idea. Scale adds reduce levels and stresses retrieval; parallel subagents trade many more tokens for wall-clock time.

## 8. The transferable pattern

Deep research is a budget-bounded, checkpointed orchestration over expensive steps. The same shape fits any agent job that runs long: a durable job record, a queue of workers, a loop with a hard budget, per-step checkpoints, compression to fit a bounded working set, and provenance carried from input to output. Code agents, data-analysis agents, and long document pipelines all reuse it.

Key idea. Long agent jobs are async jobs with a budget, checkpoints, compression, and provenance.

## Review: the 30-second answer

- Submit returns a job id; workers run the job off a queue and stream progress over SSE.

- A planner splits the question; each source is fetched, deduped, and summarized once with its source id.

- Hierarchical reduce turns summaries into findings, sections, and a report, so no call holds raw sources.

- An effort budget caps tokens, time, and searches; at the cap, the job returns a partial grounded report.

- Every step is checkpointed and idempotent, so a crashed job resumes; synthesis cites only retrieved sources.

## Quiz

Deep Research Design Quiz

Hide AllReveal All

1)Why must a deep-research job run asynchronously instead of inside one HTTP request?

Show Answer

2)Why can't the system paste all fetched pages into the synthesis prompt?

Show Answer

3)How do citations survive several levels of summarization?

Show Answer

4)Why does this design not need compensating transactions on resume?

Show Answer

5)What happens when a job hits its token cap with sub-questions left?

Show Answer

6)When does a multi-agent orchestrator-worker setup pay off?

Show Answer

## Sources and further reading

- ReAct: Synergizing Reasoning and Acting in Language Models — Yao et al. — the reason, act, observe loop the orchestrator runs.

- Introducing deep research — OpenAI — the product this problem models, and its o3-based agent trained with reinforcement learning on browsing.

- How we built our multi-agent research system — Anthropic — the orchestrator-worker variant, its 90.2% eval gain, about 15× token use, and the 80% token-variance finding.

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

Practice this problem

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

Problem statementClarifying questionsWhat makes this problem distinctiveKey conceptsThe context windowThe agent loop (ReAct)Map-reduce summarizationCheckpointingGrounding1. Requirements1.1 Functional requirements1.2 Non-functional requirements1.3 The constraint versus the property2. Back-of-the-envelope estimation2.1 Tokens per job2.2 Sources and the window2.3 Wall-clock time3. API design3.1 Submit a question3.2 Read status3.3 Stream progress3.4 Cancel3.5 Fetch the report4. Data model4.1 The research job4.2 The plan4.3 The source4.4 The finding4.5 The report and how they relate4.6 Where each entity lives5. High-level design5.1 One synchronous request5.2 Fix 1: run the research as a background job5.3 Fix 2: checkpoint each step and stream progress5.4 Fix 3: compress with map-reduce, store raw text separately5.5 Fix 4: dedup and cache sources5.6 Fix 5: enforce an effort budget5.7 The composed design6. Deep dives6.1 The agent loop and context management6.2 Cost and latency budgeting6.3 Reliability and grounding7. Variants7.1 10× scale7.2 Multi-agent orchestrator-worker7.3 Private corpus7.4 Conversational refinement8. The transferable patternReview: the 30-second answerQuizSources and further reading

Read0%

Need help?Ask about this section

On this pageProblem statement0%

Send feedback
