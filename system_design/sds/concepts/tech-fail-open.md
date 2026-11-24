---
layout: simple
title: "Fail-Open vs Fail-Closed — System Design School"
permalink: /system_design/sds/concepts/tech-fail-open
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

# Fail-Open vs Fail-Closed: Choosing a Safe Default

mediumResilienceFailure handlingRate limiting

A rate limiter keeps its counters in a shared datastore, and every request checks that store before reaching the backend. When the store goes down, each request asks a question the system can no longer answer: is this caller over its limit? The gateway must still decide — block every request, or let them all through.

This is not a bug to fix but a default to choose in advance. Any check that stands between a request and the work behind it faces the same moment: the check itself is unavailable, and the request has to go one way or the other.

## The two defaults

Fail-open means allow the request when the check is down. The backend stays reachable, but the protection the check provided is gone for as long as the outage lasts. Fail-closed means deny the request when the check is down. The protection holds, but callers see errors even though the backend itself is healthy.

Both defaults trade one property for the other. Fail-open keeps availability and drops protection. Fail-closed keeps protection and drops availability. Neither is free, so the choice is about which loss hurts less.

## How to choose

Start with one question: what does the check protect, and what happens if it stops? The answer sorts most checks cleanly.

A rate limiter guards the backend against overload and abuse. When it fails open, callers briefly face no limit. A short unlimited window is survivable; the backend has headroom, and the outage is measured in seconds. Failing closed would turn a limiter outage into a full API outage, which is a far worse result than a brief lapse in throttling. So rate limiters usually fail open.

An authentication check answers whether the caller is who they claim to be. A payment-authorization check answers whether a charge is allowed. Fail these open and anyone gets in, or any charge goes through. That is worse than returning an error. A login page that rejects everyone during an outage is a bad hour; a login page that admits everyone is a breach. So auth and payment checks fail closed.

The rule underneath: fail open when the protection is a performance guard, fail closed when it is a correctness or security guard. Compare the cost of a lapse in protection against the cost of an outage, and default toward the smaller loss.

Design checkpoint

Your authentication service is unreachable. Every incoming request needs its token validated, but the validator will not answer. Do you fail open or fail closed?

Fail open — keep the product usable during the outageFail closed — reject requests until auth recoversRetry the validator until it responds

## The middle path

The binary framing hides a third option. A pure fail-open leaves zero protection during the outage, which feels reckless for a busy system. A coarse local fallback shrinks that gap.

Each gateway instance keeps its own small limiter in memory. It cannot see traffic on other instances, so its counts are approximate. But when the shared store is down, the gateway falls back to this local limiter instead of waving everything through. Protection drops from precise to rough rather than from precise to none.

Local fallback. A gateway holding a per-instance limit of 100 requests per second, across 10 gateways, permits up to ~1,000 per second during an outage — looser than the intended global cap, but far from unbounded. The blast radius is a known multiple, not infinity.

This is fail-open with a floor. A related variant caches the last known counter state with a short time-to-live and serves those slightly stale values when the store is unreachable. Both turn "allow everything" into "allow more than usual, but bounded."

Whichever default you pick, make it loud. A silent fail-open is a hole nobody notices until it is abused. Emit a metric and an alert whenever the system enters its degraded mode, so the protection gap is visible while it lasts.

## What a strong answer sounds like

What happens to requests when your rate limiter's store is down?

BadNever considered it▾

GoodPicks one default▾

GreatChooses per what's protected, with a bounded fallback▾

## The transferable pattern

Every gating dependency needs a planned default for its own failure. Decide it by weighing two costs: the cost of a lapse in what the check protects against the cost of denying healthy traffic. Guards on performance and capacity fail open; guards on identity, money, and correctness fail closed. Where failing fully open is too loose, add a coarse local fallback to bound the blast radius, and make the degraded mode observable so it never runs silently.

This shape recurs beyond rate limiting. A circuit breaker that trips on a downstream failure must decide whether to shed the call or serve a cached default — the same fail-open versus fail-closed question. The full worked example lives in the Rate Limiter design.

Key idea. A gating check needs a default for its own outage. Pick it by what the check protects — open for capacity guards, closed for correctness guards — and bound the open case with a local fallback.

## Sources and further reading

- Rate limiting — Stripe engineering — how a production rate limiter is layered, and why availability of the limiter itself matters.

- Circuit Breaker — Martin Fowler — the pattern behind graceful degradation when a dependency is down.

- Timeouts, retries, and backoff with jitter — AWS Builders' Library — bounding calls to a failing dependency so an outage does not cascade.

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

The two defaultsHow to chooseThe middle pathWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageThe two defaults0%

Send feedback
