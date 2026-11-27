---
layout: simple
title: "Design Effort Levels in System Design — System Design School"
permalink: /system_design/sds/effort-levels
---

# Design Reasoning Effort Levels

**Difficulty:** Hard  
**Topics:** LLM serving · Scheduling & fairness · Admission control · Graceful degradation · Cost accounting

## Summary

- **Key challenge:** Keep low-effort requests fast beside high-effort ones costing 17× more; a 10% high-effort slice uses ~65% of GPU time.
- **Core design:** A resolver maps each level to a tier policy (thinking-token ceiling, latency target); effort-weighted admission feeds per-tier queues and pools; workers enforce the ceiling; a load controller caps effort; usage goes to accounting.
- **Techniques:** discrete enum (poolable, billable); budget forcing at ceiling (shallower answer, no hang); slot-weighted admission (KV memory-time); per-tier pools + min share (no starvation); cheap upward-biased router; serve min(router, load ceiling) (degrade, don't drop).

## Problem statement

Design the serving layer that lets one LLM assistant answer at different reasoning-effort levels: low, medium, high, and max. Effort is the number of internal thinking tokens the model spends before it writes the final answer. A caller picks a level per request, and the system honors it.

The scope is effort as a routing, scheduling, and budgeting dimension on top of an existing inference fleet. The base fleet mechanics are out of scope and treated as an existing dependency: continuous batching, the KV cache, and GPU economics. Model training and the model's internal reasoning method are also out of scope.

## Clarifying questions

Each question, with the assumption its answer establishes:

- Is effort explicit or automatic? Both. An explicit effort parameter is the base. An auto-router that infers effort from question difficulty is a deep dive.

- What does effort change? The thinking-token budget, and optionally the model tier.

- How many levels? A small discrete set (low, medium, high, max). Discrete tiers can be pooled, budgeted, and billed. A free-form number cannot.

- Does the response stream? Yes. The client sees a thinking phase, then the answer.

- What is the scale unit? Effort-weighted GPU-seconds, not request count.

Decode step. An LLM generates text one token at a time. Each token is one decode step: one forward pass of the model on a GPU. A 500-token reply needs about 500 decode steps, so output length is the main cost driver.

## What makes this problem distinctive

Most request-serving systems treat requests as roughly equal in cost. Here, the caller chooses the cost. A low-effort request and a max-effort request share the same endpoint, the same model, and the same GPUs, but one can run many times longer than the other.

That creates a tension. Cheap requests must feel instant, and expensive requests must still finish. If both share one queue and one pool of GPUs, long reasoning passes occupy the slots that short replies need. A second tension follows: a request that thinks longer also holds GPU memory longer, so the cost is in memory-time, not only in compute.

Key idea. The caller picks the cost of each request, so equal-slot thinking breaks: one request is not one unit of work.

## Key concepts

This section covers the concepts needed to solve this problem — prerequisites for the design work that follows.

### Thinking tokens and the answer

A reasoning model produces two phases of output. The first is the thinking phase: tokens the model writes to work through the problem, such as checking steps or trying another approach. A delimiter token then ends thinking, and the answer phase starts. Both phases cost decode steps. Only the answer is the reply the user asked for.

The thinking habit is trained into the model, not added by a prompt. DeepSeek-R1 showed that reinforcement learning, which rewards correct final answers, teaches a model to check its work and backtrack in a long chain of thought (DeepSeek-R1). The effort signal conditions how long the model thinks. The server does not inject a per-request "critique yourself" instruction. The budget only gives the trained habit room.

### The thinking budget

A thinking budget is a ceiling on thinking tokens for one request. The model may stop earlier. If it reaches the ceiling, the worker ends thinking and forces the answer. The widget runs one decode loop. Pick an effort level and a question, then press Play. An easy question stops under any budget. A hard question at low or medium effort hits the ceiling and finishes with a shallower answer.

Effort level (sets the thinking budget)

low (200)medium (1000)high (4000)

Question

easy questionhard question

thinking 0 tok · answer 0 tok

Phase

thinking

KV cache held for

0 decode steps

Reserved at admission

1300 tok

PlayReset

The red dashed line is the budget. Token counts are illustrative.

The budget is a ceiling, not a prediction. That gap matters later: the scheduler plans against the ceiling, but the bill uses the tokens actually spent.

### KV cache and memory-time

During generation, the model keeps attention state for every token so far. This state is the KV cache (key and value tensors per token per layer), and it lives in GPU memory. It grows with each token and stays until the request ends. A request that thinks for 8,000 tokens holds a large, growing block of GPU memory for the whole thinking phase.

Continuous batching runs many requests on one GPU at the same time: each decode step advances every request in the batch by one token. The batch size is often limited by KV-cache memory, not by compute. So the cost of a request is memory multiplied by time, and high effort is expensive in both.

### Effort-weighted capacity

If the fleet counts capacity in requests, one high-effort request looks like one low-effort request. It is not. Effort-weighted capacity counts each request by its budgeted cost in decode tokens (or slot-equivalents). A high-effort request with an 8,500-token ceiling counts as many slots, not one. Admission, sizing, and billing all use this unit.

Key idea. Effort is a thinking-token ceiling, and its true cost is KV memory held over time, so capacity must be counted in effort-weighted units.

## 1. Requirements

Before reading on. List the requirements, then name the one property that must not break and the one constraint that drives the design.

### 1.1 Functional requirements

- Accept and honor an effort level per request.

- Map each level to a budget: a thinking-token ceiling, an optional model tier, and a latency target.

- Stream a thinking phase, then the answer.

- Account cost per request by effort, using the thinking and answer tokens actually spent.

Auto-effort routing is covered as a deep dive. Base serving mechanics, training, and the reasoning method are out of scope.

### 1.2 Non-functional requirements

- Isolation and fairness. Low-effort requests stay fast even when the fleet is full of high-effort work.

- Per-tier latency targets. A tight first-token target for low effort. A looser, bounded target for high effort. A missed high-effort target is a degrade signal.

- Cost predictability. Budgets cap runaway thinking, and cost is attributable per tier.

- Graceful degradation. Under saturation, the system lowers effort and shrinks budgets instead of dropping requests.

- Availability. A request that exhausts its budget returns a valid, shallower answer. It does not hang or error.

### 1.3 The constraint versus the property

Isolation is the non-negotiable property. A user who asks a quick question must not wait behind someone else's long reasoning pass. The effort mix is the constraint that drives the design. It sets fleet size, admission, and the pool split. The two collide: cost efficiency wants to pack every GPU, and isolation wants headroom for cheap requests. Per-tier scheduling resolves that collision.

Key idea. Protect low-effort responsiveness; size and schedule by effort mix, not request count.

## 2. Back-of-the-envelope estimation

All inputs below are illustrative assumptions. The goal is to find which quantity actually shapes the fleet.

Requests per day1,000 M

High-effort share10 %

Answer tokens500 tok

High-effort thinking tokens8,000 tok

Decode tokens/day per GPU100 M

Real utilization50 %

Decode speed per stream50 tok/s

Share of decode tokens by tier

low

high

High vs low cost

17.0x

Decode tokens/day

1.30T

High tier share of GPU

65%

GPUs at 100%

13.0K

GPUs at real utilization

26.0K

Low / high reply time

10s / 170s

Derived from the inputs above. The defaults are illustrative, not measured.

### Cost per request

Assume a low-effort reply is about 500 decode tokens. A high-effort reply spends about 8,000 thinking tokens plus the same 500-token answer, so 8,500 tokens. One high-effort request costs 8,500 / 500 = 17× a low-effort one.

### Daily decode load

Assume 1 billion requests per day, with 90% low effort and 10% high effort.

- Low: 900M × 500 = 450B decode tokens per day.

- High: 100M × 8,500 = 850B decode tokens per day.

- Total: about 1,300B decode tokens per day.

The 10% high-effort slice uses 850 / 1,300, or about 65% of the GPU time.

### Fleet size

Assume one GPU decodes about 100M tokens per day at full utilization. Then 1,300B / 100M = 13,000 GPUs at 100%. Real fleets do not run at 100%, so at roughly 50% utilization the fleet is about 26,000 GPUs. If the mix shifts toward high effort, this number rises even when the request count stays the same.

### Latency per request

Assume one request stream decodes at about 50 tokens per second. A low-effort reply takes 500 / 50 = 10 seconds to finish. A high-effort reply takes 8,500 / 50 = 170 seconds. That is why high-effort requests hold slots and memory far longer.

The fixed system prompt costs little at the margin. Prefix caching reuses the computed attention state of a shared prompt prefix across requests, so effort, not the prompt, is the marginal cost.

Key idea. A 10% high-effort slice can use about 65% of the GPU time, so fleet size follows the effort-weighted sum, not the request count.

## 3. API design

Design checkpoint

Should the API take effort as an enum (low, medium, high, max) or as a raw thinking-token count?

A raw token count, so callers get exact controlAn enum, because tiers are the unit for pools, budgets, and billing

The calls follow the life of a request: discover the tiers, submit, stream, and cancel.

GET/v1/effort-tiers

Request & response

This returns the config-backed catalog for each level. Clients read it instead of hardcoding what "high" means, so operators can change a budget without a client release.

POST/v1/responses

Request & response

The response streams in two phases. The usage event reports the tokens actually spent. The done event's finish_reason tells the client whether the model stopped on its own (stop) or hit the ceiling (budget_exhausted). The caller's identity and plan come from the authenticated session, not the body.

POST/v1/responses/{id}/cancel

Request & response

Cancel aborts an in-flight generation and frees its GPU slot and KV memory. This matters most for high effort, because an abandoned long reasoning pass wastes the most GPU time.

Key idea. Expose effort as a discrete enum, report actual spend in the stream, and make cancellation cheap.

## 4. Data model

Start with the request itself.

A Request is transient. It waits in a queue, lives in GPU memory while it decodes, and then disappears. It names a level, but it cannot say what that level means. That needs a policy.

EffortTier maps each level to a thinking-token ceiling, a model tier, and a latency target. It is small, it changes rarely, and admission reads it. It still cannot say where a request runs or how much of the fleet a tier may use. That is a scheduler setting.

TierPool is scheduler configuration, not a database row: a per-tier queue, a GPU share, a concurrency cap, and a minimum share. None of these records the real cost of a request, because the budget is only a ceiling. That needs an accounting record.

Usage is append-only. It records what the request actually spent, which is what billing and capacity planning need.

Each tier has one pool and serves many requests. Each finished request writes one usage record. The KV cache is deliberately not modeled: it is in-memory attention state on a GPU, and its effect is a system property (memory-time), not a stored entity. The slot weight of a request is computed at admission and is not persisted either.

Storage follows the access pattern. EffortTier lives in a control-plane config store. TierPool lives in scheduler config. Request lives in queues and GPU memory. Usage goes to an append-only accounting store.

Key idea. Separate the policy (tier), the placement (pool), the transient work (request), and the truth (usage), because the budget is only a ceiling.

## 5. High-level design

Reading the diagrams. Components added in each step have a dashed pink outline and a NEW badge.

### 5.1 One fixed generation path

The starting point is a stateless API tier in front of the existing GPU fleet. Every request gets the same generation settings.

This fails the first requirement. Some users want a quick, cheap answer. Others want a slow, deep one. One fixed path gives every user the same depth, and it puts no ceiling on how long the model thinks.

### 5.2 Resolve effort to a tier policy

Add an effort resolver that reads the request's effort and looks up the tier in a control plane. The worker receives an enforced thinking budget with the request.

Users can now choose depth. But the fleet still admits requests one per slot. A high-effort request holds GPU and KV memory roughly 17 times longer than a low one, so a burst of them fills the batch and memory with work the admission logic counted as small.

### 5.3 Effort-weighted admission

Add admission control that charges each request its budgeted cost in slot-equivalents, plus a global load cap. A high-effort request now counts as many slots, so the fleet cannot silently accept more work than its memory can hold.

Admission is now accurate, but it still feeds one queue. When a burst of high-effort work arrives, it takes the free slots first. Low-effort requests queue behind it, and their first token arrives late.

### 5.4 Per-effort queues and pools

Add per-effort queues that feed a weighted scheduler. Each tier gets a GPU share sized to its latency target, so a high-effort burst slows high-effort work only.

Tiers are isolated. But someone still has to pick the level, and callers often judge difficulty poorly. A user who leaves every request on "high" wastes GPU time on easy questions.

### 5.5 Explicit effort or an auto-router

Add an optional auto-router: a small, cheap classifier that proposes an effort level from the question when the caller does not set one. An explicit parameter still wins.

Effort is now chosen well in normal conditions. Under saturation, though, every tier's queue grows. Rejecting requests breaks the availability requirement.

### 5.6 Degrade by lowering effort, then account

Add a load controller that lowers the effective effort ceiling under saturation and shrinks budgets, and an accounting store that receives a usage record when each request finishes.

This is the composed design. The request path for one high-effort call is below.

Key idea. Each component answers one failure: a tier policy for choice, weighted admission for true cost, per-tier pools for isolation, a router for selection, and a load controller for saturation.

## 6. Deep dives

### 6.1 Effort as a thinking-token budget

Before reading on. The scheduler must admit a request before it knows how long the model will think. What number should it plan against, and what happens at the ceiling?

The thinking phase has a deliberately wide range of lengths. The effort level gives that range a known ceiling, which is what lets the scheduler plan. Enforcement lives in the decode loop on the worker. After each step, the worker checks the thinking-token count. At the ceiling, it ends thinking and forces the answer, and the stream finishes with budget_exhausted. So the degraded case is a shallower answer, not a hang.

The s1 paper describes this control as budget forcing (s1: Simple test-time scaling). It gives two levers. To truncate, the decoder inserts the end-of-thinking delimiter. To extend, the decoder suppresses the delimiter and appends a continuation cue. The paper's example appends "Wait", which makes the model re-check its count of letters in a word.

Design checkpoint

Most generations stop well under their ceiling. Should admission reserve the full budget or the expected length?

Reserve the expected length and admit moreReserve the full budget, or reserve less and preempt when memory runs short

Admission estimates the budgeted remaining tokens per request. That is deliberate over-reservation, because many generations stop under the cap. It wastes some capacity but never runs out of KV memory mid-request. The alternative is optimistic admission with preemption: admit more, and when memory runs short, pause a request and free its KV cache to resume later. Preemption raises utilization but adds latency spikes to the preempted request.

A top tier has another option: parallelize instead of thinking longer. The worker samples several independent reasoning chains and then takes a majority vote or asks a judge model to pick one. Self-consistency showed that a majority vote over sampled chains improves reasoning accuracy (Self-Consistency). This trades one long KV hold for several shorter ones, but it multiplies the concurrent slots the request uses.

Monitor the per-tier distribution of thinking tokens, KV occupancy by tier, the budget-exhaustion rate, and effort-weighted GPU utilization. A rising exhaustion rate means the budgets are too small for the questions the tier receives.

What separates answers — the thinking budget

BadTreats effort as a prompt tweak▾

GoodEnforces a token ceiling in the decode loop▾

GreatPlans memory-time and names the reservation trade-off▾

### 6.2 Scheduling and fairness

Before reading on. A burst of high-effort requests arrives. With one shared queue, what happens to the first-token latency of low-effort requests? What stops the reverse case?

With one shared queue, a high-effort burst takes the free slots, and each of those slots stays busy for a long time. Low-effort requests wait behind them. The widget models this with 10 slots and a high request that holds a slot 17 times longer than a low one. Run the shared queue first, then the pooled mode.

One shared queuePer-effort pools + min share

GPU slots (tick 0; high-effort burst at ticks 5 to 14)

idle

idle

idle

idle

idle

idle

idle

idle

idle

idle

Queued low

0

Queued high

0

Low first-token wait (recent avg)

0.0 ticks

PlayReset

A toy model: 10 slots, a high request holds a slot 17 times longer than a low one, and pooled mode keeps 4 slots for low effort.

Per-effort pools isolate the tiers. Each pool gets a queue and a GPU share sized to its latency target. One alternative is a single weighted fair scheduler, in which a high-effort dequeue consumes more budgeted slots than a low-effort one. Both approaches make a single high-effort request pay for the capacity it really uses, so it cannot quietly take the capacity of ten cheap ones.

Starvation can happen in both directions. A flood of high-effort work can starve low effort. An endless stream of cheap requests can also starve high effort, because a scheduler that prefers short jobs would never dispatch a long one. A minimum share per pool bounds both cases: each tier always gets at least its floor of the fleet, and it can borrow idle capacity above that floor.

Each tier has its own latency target. A breach of the loose high-effort target is a signal to degrade, not a reason to page an engineer. The blast radius of a high-effort spike becomes "deep answers slow down", not "the assistant stalls". Monitor per-tier queue depth, first-token and completion latency, actual versus target GPU share, and min-share violations.

What separates answers — scheduling

BadOne queue, one slot per request▾

GoodPer-tier pools or weighted fair scheduling▾

GreatTwo-way anti-starvation and tier-aware alerting▾

### 6.3 Auto-effort routing and degradation

Before reading on. A router can send a question to the wrong effort level in two directions. Are the two mistakes equally costly? And when the fleet saturates, who wins: the router or the load controller?

An explicit parameter is honest, but callers judge difficulty poorly. An auto-router assigns effort from predicted difficulty. It must cost little compared with what it saves, so it is a small classifier or a heuristic, never a large generation. OpenAI describes a similar design for GPT-5: a real-time router chooses between a fast model and a deeper reasoning model based on the conversation (Introducing GPT-5).

Mis-routes have asymmetric costs. Routing up wastes GPU-seconds. Routing down returns an under-thought, worse answer, which costs the user. So the router biases toward higher effort, and the client offers a "think harder" retry that resubmits at the next tier.

Design checkpoint

The router proposes high effort, but the fleet is saturated. What level should the request run at?

The router's proposal, because quality comes firstThe minimum of the router's proposal and the load ceiling

Degradation is the pressure-relief valve. Under saturation, the load controller lowers the global effective ceiling: max is served as high, and high is served as medium. It can also shrink the budgets within each tier. The response tells callers that their request was capped. The final budget is the minimum of the router's proposal and the load ceiling. The widget steps through a load spike and shows the served level at each step.

Fleet load as % of effort-weighted capacity (step 1 of 16)

Load

40%

Router proposes

max

Load ceiling

max

Served = min(both)

max

PlayStepReset

Thresholds and the load curve are illustrative. No request is dropped; only its effort is lowered.

Monitor whether high-routed queries used their budget, the retry rate (a rising rate signals under-routing), the frequency of effort-cap events, and answer quality per tier.

What separates answers — routing and degradation

BadLarge-model router or drop under load▾

GoodCheap router and an effort cap under load▾

GreatAsymmetric bias, retry path, and min of proposal and ceiling▾

### 6.4 Failure modes

Each failure has a contained outcome and a metric that detects it.

FailureOutcomeDetected by

Budget exhaustionValid, shallower answerExhaustion rate per tier

High-effort spikeSlows the high pool onlyPer-tier queue depth

Starvation in either directionBounded by min shareMin-share violation alarm

Router under-routingWorse answers, then retriesRetry rate, per-tier quality

Runaway thinkingStopped at the ceilingThinking-token distribution

Abandoned long requestSlot reclaimedCancel rate

Key idea. Budgets make cost finite, pools make it isolated, and the min of router and load ceiling makes saturation lower depth instead of dropping work.

## 7. Variants

### 10× scale

The fleet follows the effort-weighted sum, so the mix matters more than the count. The levers are quantization (lower-precision weights, which cut memory and raise throughput), speculative decoding (a small draft model proposes several tokens and the large model verifies them in one step), tighter budgets, and better routing.

### A heavier max tier

A deep-research tier has budgets measured in minutes. It gets its own pool and asynchronous delivery: the client submits, then polls or receives a notification, instead of holding a live stream open.

### Per-user or per-plan caps

Admission clamps the requested level to the plan's maximum. For example, a free plan may be capped at medium. Effort then becomes both a quality dial and a pricing dial.

Key idea. At larger scale, change the mix and the per-token cost; for the heaviest tier, change the delivery model.

## 8. The transferable pattern

Turn the cost dial into a small set of discrete tiers. Weight admission by the true cost of each tier. Isolate the tiers with pools and minimum shares. Choose the tier explicitly or with a cheap router. Under load, degrade by lowering the dial, not by dropping work. The same shape applies to priced query tiers in a database service, batch versus interactive analytics, and coding agents that run at different effort levels.

Key idea. When callers choose the cost of their own requests, make cost a first-class scheduling unit.

## Review

- Effort is a thinking-token ceiling. Its true cost is KV memory held over time.

- A 10% high-effort slice can use about 65% of the GPU time, so size by effort mix.

- Expose effort as an enum, stream thinking then answer, and report actual usage.

- Enforce the budget in the decode loop; at the ceiling, force the answer with budget_exhausted.

- Admit by budgeted cost, and isolate tiers with per-effort pools and a two-way min share.

- Route with a cheap classifier biased upward; serve the minimum of the router's proposal and the load ceiling.

## Quiz

Reasoning Effort Levels Quiz

Hide AllReveal All

1)Why should fleet capacity be measured in effort-weighted GPU-seconds instead of requests per second?

2)Why is a high-effort request expensive in memory, not only in compute?

3)What happens when a request reaches its thinking budget?

4)Why does a minimum share per pool protect both tiers?

5)Why should an auto-router bias toward higher effort?

6)Under saturation, how is the served effort level computed, and why not reject requests?

## Sources and further reading

- Reasoning models guide — OpenAI — the reasoning-effort parameter and reasoning tokens as billed output.

- Extended thinking — Anthropic — thinking budgets and the separate thinking and answer phases in a streamed response.

- s1: Simple test-time scaling — budget forcing: truncating with the delimiter or extending with "Wait".

- DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning — how reinforcement learning trains long chain-of-thought reasoning.

- Self-Consistency Improves Chain of Thought Reasoning in Language Models — sampling several reasoning chains and taking a majority vote.

- Introducing GPT-5 — OpenAI — a real-time router that chooses between a fast model and a deeper reasoning model.
