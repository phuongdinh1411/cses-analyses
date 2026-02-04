---
layout: simple
title: "Design [System Name]"
permalink: /system_design/design-[system-name]
---

# Design [System Name]

Brief 2-3 sentence overview of the system. What does it do? Why is it challenging at scale?

> **Interview context**: This is a common system design question. Focus on [key challenge] and be ready to discuss trade-offs around [main trade-off area].

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Core Components](#3-core-components)
4. [Data Model](#4-data-model)
5. [Key Design Decisions](#5-key-design-decisions)
6. [Scalability](#6-scalability)
7. [Reliability](#7-reliability)
8. [Interview Tips](#8-interview-tips)
9. [Key Takeaways](#9-key-takeaways)

---

## 1. Requirements

> **Interview context**: Always start by clarifying requirements. Don't assume—ask questions to understand the scope.

### Questions to Ask the Interviewer

- What's the expected scale? (users, QPS, data size)
- What are the latency requirements?
- Is consistency or availability more important?
- What features are must-have vs nice-to-have?

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Core Feature 1** | Description of what it does |
| **Core Feature 2** | Description of what it does |
| **Core Feature 3** | Description of what it does |

### Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| **Availability** | 99.99% | Business critical service |
| **Latency** | p99 < 200ms | User experience |
| **Throughput** | 100K QPS | Expected peak load |
| **Data retention** | 5 years | Compliance requirement |

### Capacity Estimation

```
Users:           100 million
Daily active:    10 million
Requests/day:    ~1 billion
QPS (average):   ~12K
QPS (peak):      ~50K (4x average)

Storage:
- Per record:    ~500 bytes
- Daily growth:  ~500 GB
- 5-year total:  ~1 PB
```

---

## 2. High-Level Architecture

> **Interview context**: "Let me draw the high-level architecture first, then we can dive into specific components."

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                  │
│              (Web, Mobile, API consumers)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                               │
│                   (DNS, CDN, L7 LB)                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                 │
│           (Rate limiting, Auth, Routing)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Service  │   │ Service  │   │ Service  │
        │    A     │   │    B     │   │    C     │
        └──────────┘   └──────────┘   └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Cache   │   │ Database │   │  Queue   │
        │ (Redis)  │   │ (MySQL)  │   │ (Kafka)  │
        └──────────┘   └──────────┘   └──────────┘
```

### Component Responsibilities

| Component | Responsibility | Technology Choice |
|-----------|---------------|-------------------|
| **Load Balancer** | Distribute traffic, SSL termination | AWS ALB / Nginx |
| **API Gateway** | Rate limiting, authentication | Kong / AWS API Gateway |
| **Service A** | [Primary function] | [Language/Framework] |
| **Cache** | Reduce database load | Redis Cluster |
| **Database** | Persistent storage | MySQL / PostgreSQL |
| **Queue** | Async processing | Kafka / SQS |

---

## 3. Core Components

### 3.1 [Component Name]

> **Interview context**: "Let me explain how [component] works..."

#### The Challenge

[Explain the problem this component solves]

#### Options

| Option | Pros | Cons |
|--------|------|------|
| Option A | Pro 1, Pro 2 | Con 1, Con 2 |
| Option B | Pro 1, Pro 2 | Con 1, Con 2 |
| Option C | Pro 1, Pro 2 | Con 1, Con 2 |

#### Our Approach

[Explain chosen approach and why]

```
[Pseudocode or diagram explaining the concept - max 15 lines]
```

#### Why Not [Alternative]?

[Address the obvious alternative that wasn't chosen]

> **Interviewer might ask**: "[Common follow-up question]?"
>
> [Answer explaining the nuance]

---

### 3.2 [Next Component]

[Repeat the same pattern: Challenge → Options → Approach → Why Not X]

---

## 4. Data Model

> **Interview context**: "For the database schema, let me think about the access patterns we need to support..."

### Schema Design

```sql
-- Main entity table
CREATE TABLE [entity] (
    id              BIGINT PRIMARY KEY,
    [field_1]       VARCHAR(255) NOT NULL,
    [field_2]       TIMESTAMP NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_field_1 ([field_1])
);

-- Related entity
CREATE TABLE [related_entity] (
    id              BIGINT PRIMARY KEY,
    [entity]_id     BIGINT REFERENCES [entity](id),
    [field]         VARCHAR(255),
    INDEX idx_entity ([entity]_id)
);
```

### Access Patterns

| Query | Frequency | Index Used |
|-------|-----------|------------|
| Get by ID | Very High | Primary key |
| Search by [field] | High | idx_field_1 |
| List by [entity] | Medium | idx_entity |

> **Interviewer might ask**: "Why did you choose [SQL/NoSQL]?"
>
> [Explain based on access patterns, consistency needs, scale requirements]

---

## 5. Key Design Decisions

### 5.1 [Decision Area 1]

> **Interview context**: "One key decision is [area]..."

| Option | Trade-off |
|--------|-----------|
| **Option A** | Better for X, worse for Y |
| **Option B** | Better for Y, worse for X |

**We chose Option A because**: [Justification based on requirements]

### 5.2 [Decision Area 2]

[Same pattern]

### Design Decisions Summary

| Decision | Choice | Alternative | Rationale |
|----------|--------|-------------|-----------|
| [Area 1] | [Choice] | [Alt] | [Why] |
| [Area 2] | [Choice] | [Alt] | [Why] |
| [Area 3] | [Choice] | [Alt] | [Why] |

---

## 6. Scalability

> **Interview context**: "Let me discuss how this system scales..."

### Horizontal Scaling

```
                    Load Balancer
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ Server 1│      │ Server 2│      │ Server N│
    └─────────┘      └─────────┘      └─────────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
                   ┌──────┴──────┐
                   ▼             ▼
              ┌────────┐   ┌────────┐
              │ Shard 1│   │ Shard N│
              └────────┘   └────────┘
```

### Scaling Strategies

| Component | Strategy | When to Apply |
|-----------|----------|---------------|
| API Servers | Horizontal scaling | CPU > 70% |
| Database | Read replicas, then sharding | Read QPS > X |
| Cache | Cluster mode | Memory > 80% |

### Bottlenecks and Mitigations

| Bottleneck | Symptom | Mitigation |
|------------|---------|------------|
| Database writes | High latency | Write-behind cache, async processing |
| Single hot key | Cache miss storm | Local cache, key spreading |
| Network | High latency | CDN, edge caching |

---

## 7. Reliability

> **Interview context**: "For reliability, let's discuss failure scenarios..."

### Failure Scenarios

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| Server crash | Partial unavailability | Auto-scaling, health checks |
| Database failure | Data unavailable | Read replicas, failover |
| Network partition | Split brain | Consensus protocol |
| Datacenter outage | Regional unavailability | Multi-region deployment |

### Recovery Procedures

1. **Detection**: Health checks every 10s, alerting on failure
2. **Failover**: Automatic promotion of replica (< 30s)
3. **Recovery**: Rebuild failed node, catch up from leader

---

## 8. Interview Tips

### Approach (45 minutes)

```
0-5 min:   CLARIFY REQUIREMENTS
           - Ask about scale, latency, consistency needs
           - Identify must-have vs nice-to-have features

5-10 min:  CAPACITY ESTIMATION
           - Users, QPS, storage
           - Identify the scale we're designing for

10-25 min: HIGH-LEVEL DESIGN
           - Draw main components
           - Explain data flow
           - Discuss API design

25-40 min: DEEP DIVE
           - Pick 2-3 areas to explore in detail
           - Discuss trade-offs for each decision
           - Address failure scenarios

40-45 min: WRAP UP
           - Summarize key decisions
           - Discuss future improvements
           - Answer remaining questions
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "Use a database" | "Given the read-heavy workload, I'd start with a relational database with read replicas" |
| "Add caching" | "We can add a cache layer with a TTL of X based on how stale the data can be" |
| "Scale horizontally" | "At this QPS, we'd need N servers assuming each handles Y requests/second" |

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "How would you handle [edge case]?" | Discuss specific mitigation strategy |
| "What if scale increases 10x?" | Explain what breaks first and how to fix |
| "How do you ensure consistency?" | Discuss consistency model and trade-offs |
| "What metrics would you monitor?" | Latency percentiles, error rates, saturation |

---

## 9. Key Takeaways

### Core Concepts

1. **[Concept 1]**: One-sentence explanation
2. **[Concept 2]**: One-sentence explanation
3. **[Concept 3]**: One-sentence explanation

### Trade-offs to Remember

| Trade-off | When to choose A | When to choose B |
|-----------|------------------|------------------|
| [A vs B] | [Scenario] | [Scenario] |
| [C vs D] | [Scenario] | [Scenario] |

### Red Flags to Avoid

- Don't skip requirements clarification
- Don't dive into code before architecture
- Don't ignore failure scenarios
- Don't forget to discuss trade-offs

---

## References

- [Relevant paper or blog post](URL)
- [Related system design](URL)
- [Official documentation](URL)
