# System Design Interview-Style Template

This template defines the canonical format for system design documents that follow an **interview discussion flow** rather than a solution-presentation approach.

---

## Core Principles

### 1. Problem Before Solution

**Never present a solution without first establishing the problem it solves.**

```
❌ BAD: "We use consistent hashing to distribute data."

✅ GOOD: "A single server can't store petabytes of data. We need to split
         data across nodes. Simple modulo hashing (hash % N) has a problem:
         adding a node remaps almost ALL keys. Consistent hashing solves
         this by only remapping ~1/N keys."
```

### 2. Discussion Over Presentation

**Frame technical decisions as discussions, not declarations.**

Use these patterns:
- "The challenge here is..."
- "We have several options..."
- "Why not just use X? Because..."
- "The trade-off is..."

### 3. No Implementation Code

**Remove all implementation code.** Keep only:
- Pseudocode that explains concepts (max 10-15 lines)
- API signatures/interfaces
- Configuration examples

```
❌ BAD: Full Python class with __init__, methods, error handling

✅ GOOD: Pseudocode showing the algorithm concept:
         for each node in ring.walk_clockwise(key):
             if node.is_healthy():
                 return node
```

---

## Required Sections

### 1. Interview Context Callouts

Use blockquotes to set up interview transitions:

```markdown
> **Interview context**: After discussing high-level design, the interviewer
> will likely ask: "How do you distribute data across nodes?"
```

Place these before each major topic transition.

### 2. The Problem/Challenge Framing

Before every solution, explain WHY it's needed:

```markdown
### The Challenge

With replication, we introduced a new problem: **keeping replicas consistent**.

What happens if:
- Client 1 writes x=1 to Node A
- Client 2 writes x=2 to Node B (before A replicates)
- Client 3 reads from Node C

Which value does Client 3 see?
```

### 3. Options Discussion

Present alternatives before recommending one:

```markdown
### Options for ID Generation

| Option | Pros | Cons |
|--------|------|------|
| UUID | Simple, no coordination | 128 bits, not sortable |
| Auto-increment | Sortable, compact | Single point of failure |
| Snowflake | Sortable, distributed | Clock sync complexity |

For our use case (need sortable, distributed), **Snowflake** makes sense because...
```

### 4. "Why Not X?" Sections

Address obvious alternatives explicitly:

```markdown
#### Why Not Just Use a Database Auto-Increment?

At first glance, this seems simplest. But consider:
- Single point of failure (the database)
- Network round-trip for every ID
- Scalability bottleneck at high QPS

For 10K IDs/second across multiple services, we need a distributed approach.
```

### 5. "Interviewer Might Ask" Prompts

Anticipate follow-up questions:

```markdown
> **Interviewer might ask**: "What happens if two datacenters generate IDs
> with the same timestamp?"

Good question! The datacenter ID in bits 12-21 ensures uniqueness even with
identical timestamps. Two datacenters would produce:
- DC1: timestamp|01|sequence
- DC2: timestamp|02|sequence
These are guaranteed different.
```

### 6. Trade-off Tables

Summarize decisions with clear trade-offs:

```markdown
| Decision | We Chose | Alternative | Why |
|----------|----------|-------------|-----|
| Consistency | Eventual | Strong | 99.99% availability requirement |
| Partitioning | Hash | Range | No range query requirement |
| Storage | LSM | B-Tree | Write-heavy workload |
```

---

## Document Structure

```markdown
# System Design: [Topic]

Brief 2-3 sentence overview of what we're designing.

---

## Table of Contents
[Standard TOC]

---

## Requirements

### Functional Requirements
[Table format]

### Non-Functional Requirements
[Table with targets: latency, availability, scale]

### Capacity Estimation
[Back-of-envelope calculations]

---

## High-Level Architecture

> **Interview context**: "Let me start with the basic architecture..."

[ASCII diagram]

### Components
[Table explaining each component's responsibility]

---

## [Topic 1: e.g., Data Partitioning]

> **Interview context**: [Transition phrase]

### The Challenge
[Why do we need this?]

### Options
[Table comparing approaches]

### Our Approach
[Chosen solution with justification]

#### Why Not [Alternative]?
[Address obvious alternatives]

> **Interviewer might ask**: [Anticipated question]
[Answer]

---

## [Topic 2: e.g., Replication]
[Same pattern...]

---

## Trade-offs and Design Decisions

### Summary Table
[All major decisions in one table]

### When to Choose What
[Use case → configuration recommendations]

---

## Interview Tips

### Approach Flow
[Suggested 45-minute breakdown]

### Key Phrases
[Instead of X, say Y table]

### Common Follow-ups
[Question → key points table]

---

## References
[Links to papers, related docs]
```

---

## What to Remove

### 1. Full Implementation Code

Remove complete class implementations. Replace with:
- Conceptual pseudocode (10-15 lines max)
- Interface/API definitions
- Algorithm descriptions in prose

### 2. Language-Specific Details

Remove:
- Import statements
- Type annotations (unless they clarify the concept)
- Error handling boilerplate
- Logging/metrics code

### 3. Configuration Boilerplate

Keep only configuration that illustrates a concept:

```
❌ BAD: Full YAML config with 50 fields

✅ GOOD: Key parameters table:
         | Parameter | Value | Why |
         |-----------|-------|-----|
         | W (write quorum) | 2 | Balance of durability and latency |
```

---

## Acceptable Pseudocode

Pseudocode is acceptable when it clarifies an algorithm:

```python
# Finding nodes for a key (conceptual)
def get_nodes_for_key(key, n_replicas=3):
    position = hash(key)
    nodes = []
    for node in ring.walk_clockwise_from(position):
        if node not in nodes:
            nodes.append(node)
        if len(nodes) == n_replicas:
            break
    return nodes
```

This is acceptable because:
- It's short (10 lines)
- It explains the CONCEPT, not implementation details
- No error handling, types, or boilerplate

---

## ASCII Diagrams

Use ASCII diagrams liberally for:
- Architecture overviews
- Data flow sequences
- State machines
- Comparison visualizations

```
Example - Hinted Handoff Flow:

Normal:     Client → [A, B, C] → Success
With B down: Client → [A, C, D(hint for B)] → Success
Recovery:   D → B (deliver hint) → Delete hint
```

---

## Checklist for Each Document

Before marking a document complete:

- [ ] Every solution has a preceding "challenge" or "problem" section
- [ ] All implementation code removed (only pseudocode remains)
- [ ] "Interview context" callouts before major sections
- [ ] "Why not X?" addresses obvious alternatives
- [ ] "Interviewer might ask" for complex topics
- [ ] Trade-off summary table exists
- [ ] Interview tips section with approach flow
- [ ] ASCII diagrams explain complex concepts
- [ ] No language-specific boilerplate
