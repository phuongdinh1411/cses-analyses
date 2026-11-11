# 🏦 WorldQuant Senior SWE — 2-Month Interview Prep Plan

> **Target Role:** Senior Software Engineer @ WorldQuant  
> **Timeline:** 8 Weeks  
> **Start Date:** ___________  
> **Interview Date:** ___________

---

## 🔍 What WorldQuant Actually Tests

WorldQuant is a **quantitative hedge fund** (~$90B AUM). Their SWE roles sit at the intersection of **high-performance engineering + quant finance**.

> ⚡ **Based on actual job descriptions scraped Nov 2025** — see Research Findings section below for full JD details.

| Area | Weight | My Current Level (1–5) |
|---|---|---|
| Data Structures & Algorithms | ⭐⭐⭐⭐⭐ | |
| Python (production-grade, internals) | ⭐⭐⭐⭐⭐ | |
| System Design (distributed, ETL, data pipelines) | ⭐⭐⭐⭐⭐ | |
| Database / SQL (PostgreSQL, query optimization) | ⭐⭐⭐⭐⭐ | |
| API Design (REST / gRPC) | ⭐⭐⭐⭐ | |
| Network Protocols & Secure Communication | ⭐⭐⭐⭐ | |
| Data Engineering (ETL/ELT, Kafka, Airflow) | ⭐⭐⭐⭐ | |
| AI/LLM tooling (agentic workflows) | ⭐⭐⭐⭐ | |
| DevOps (Docker, CI/CD, observability) | ⭐⭐⭐ | |
| Quant/Finance domain awareness | ⭐⭐⭐ | |
| Behavioral / leadership / mentoring | ⭐⭐⭐ | |

---

## 📅 Month 1 — Foundations & Core Skills

### ✅ Week 1–2: Python Mastery (Senior Level)

> Based on JD: _"Mastery of Python internals, concurrency, performance profiling, packaging, FastAPI/Flask, SQLAlchemy, pytest, mypy"_

- [ ] **Advanced Python**: generators, decorators, context managers, metaclasses, descriptors
- [ ] **Concurrency**: `threading`, `multiprocessing`, `asyncio`, GIL implications, `concurrent.futures`
- [ ] **Performance**: `numpy`, `pandas`, profiling with `cProfile`, memory optimization, avoiding GIL bottlenecks
- [ ] **Testing**: `pytest`, mocking, property-based testing with `hypothesis`, test fixtures
- [ ] **Type hints**: `mypy`, `Protocol`, generics, type narrowing
- [ ] **Frameworks**: `FastAPI` (build a REST API), `SQLAlchemy` (ORM + raw SQL), `Flask` basics
- [ ] **Packaging**: `pyproject.toml`, virtual envs, `pip`, `poetry`
- [ ] **AI tooling**: practice using GitHub Copilot / Cursor / LLM agents in your workflow

**Key resource:** _Fluent Python_ by Luciano Ramalho (2nd ed.)

#### Notes & Learnings:
> _Add your notes here as you go_

---

### ✅ Week 3–4: Data Structures & Algorithms

**Target:** 3–5 LeetCode problems/day — Medium focus, mix in Hard  
**LeetCode lists:** Blind 75 → NeetCode 150

| Topic | Status | Key Problems Solved |
|---|---|---|
| Arrays / Sliding Window | ⬜ | |
| Two Pointers | ⬜ | |
| Prefix Sums | ⬜ | |
| Trees / BFS / DFS | ⬜ | |
| Graphs / Dijkstra | ⬜ | |
| Topological Sort | ⬜ | |
| Heaps / Priority Queues | ⬜ | |
| Dynamic Programming (1D) | ⬜ | |
| Dynamic Programming (2D) | ⬜ | |
| Binary Search | ⬜ | |
| Sorting (custom comparators) | ⬜ | |

#### Problem Log:
| Date | Problem | Difficulty | Outcome | Notes |
|---|---|---|---|---|
| | | | | |

---

## 📅 Month 2 — System Design + Quant Domain + Mock Interviews

### ✅ Week 5–6: System Design (Quant-Finance Flavor)

#### Core Concepts to Master (aligned with real JDs):
- [ ] **ETL/ELT pipeline design** — this is the #1 system design topic in their JDs
- [ ] **Data streaming**: Kafka, event-driven architecture, producer/consumer patterns
- [ ] **Data orchestration**: Apache Airflow (DAGs, task dependencies, retries)
- [ ] **Distributed systems**: CAP theorem, consistent hashing, sharding, fault tolerance
- [ ] **Caching strategies**: Redis, in-memory lookup, cache invalidation
- [ ] **API design**: REST vs gRPC, clean and well-documented interfaces
- [ ] **Observability**: OpenTelemetry, Grafana, ELK stack, structured logging, distributed tracing
- [ ] **DevOps**: Docker, CI/CD (GitLab CI / Jenkins), Infrastructure-as-Code (Terraform/Ansible)

#### System Design Problems to Practice (directly from JD themes):
- [ ] Design a **large-scale ETL pipeline** that processes financial data (batch + streaming)
- [ ] Design a **data ingestion & normalization system** for multiple market data sources
- [ ] Design a **backtesting engine** for trading strategies
- [ ] Design an **event-driven alpha signal computation pipeline**
- [ ] Design a **portfolio risk calculation system** (distributed, low-latency)
- [ ] Design a **data warehouse** with point-in-time correctness
- [ ] Design a **microservice API** with observability (tracing, metrics, logging)
- [ ] Design a **workflow orchestration system** (like Airflow)

**Key resources:**
- _Designing Data-Intensive Applications_ by Martin Kleppmann — read chapters on data pipelines & stream processing
- ByteByteGo, Grokking System Design

#### System Design Notes:
> _Add your design sketches and key decisions here_

---

### ✅ Week 7: Quant Finance Fundamentals

- [ ] **Alpha factors**: what they are, how they're researched (WorldQuant Brain platform)
- [ ] **Backtesting concepts**: look-ahead bias, overfitting, Sharpe ratio, drawdown
- [ ] **Market microstructure**: order books, bid/ask spread, market impact
- [ ] **Time series**: stationarity, autocorrelation, rolling windows, OHLCV data
- [ ] **Risk metrics**: VaR, beta, correlation matrices, factor models

**Practice:** Explore [WorldQuant Brain Platform](https://platform.worldquant.com/) — build a few alphas.

#### Quant Finance Notes:
> _Add your notes here_

---

### ✅ Week 8: Mock Interviews + Behavioral

#### Behavioral (STAR Format) — Senior-Level Themes:
- [ ] Describe a system you designed from scratch under constraints
- [ ] How did you handle a production incident / data corruption?
- [ ] How do you mentor junior engineers?
- [ ] Tell me about a time you disagreed with a technical decision
- [ ] How do you balance speed vs. correctness?

#### My STAR Stories:
| Theme | Situation | Task | Action | Result |
|---|---|---|---|---|
| System Design | | | | |
| Production Incident | | | | |
| Mentorship | | | | |
| Technical Disagreement | | | | |
| Speed vs. Correctness | | | | |

#### Mock Interview Log:
| Date | Type | Platform | Outcome | Feedback |
|---|---|---|---|---|
| | DSA | | | |
| | System Design | | | |

---

## 🗂️ Weekly Study Schedule

```
Mon  → LeetCode (2 problems) + Python deep-dive
Tue  → LeetCode (2 problems) + System Design reading
Wed  → LeetCode (2 problems) + Quant finance concept
Thu  → System Design practice (design one full system)
Fri  → LeetCode hard problem + mock interview
Sat  → WorldQuant Brain platform / project work
Sun  → Review week's notes + behavioral prep
```

---

## 🛠️ Resources

| Category | Resource | Status |
|---|---|---|
| Python Advanced | _Fluent Python_ (Ramalho), Real Python | ⬜ |
| DSA | LeetCode, NeetCode.io | ⬜ |
| DSA Theory | _CLRS_ Introduction to Algorithms | ⬜ |
| System Design | _DDIA_ (Kleppmann) | ⬜ |
| System Design | ByteByteGo, Grokking System Design | ⬜ |
| Quant Finance | WorldQuant Brain Platform | ⬜ |
| Quant Finance | _Quantitative Finance with Python_ (Fabozzi) | ⬜ |
| Mock Interviews | interviewing.io, Pramp, Exponent | ⬜ |
| kdb+/q | code.kx.com (free tutorials) | ⬜ |

---

## ⚡ WorldQuant-Specific Tips

> All tips below are derived from **real job descriptions** (Nov 2025), not assumptions.

1. **"Intellectual horsepower first"** — they explicitly say this. Show depth of thinking, not just correct answers.
2. **AI/LLM fluency is NOW required** — multiple JDs mention LLM agents, AI copilots, agentic tooling as *daily workflow*. Know how to use AI coding tools effectively.
3. **High autonomy is tested** — they want self-directed engineers. Demonstrate ownership in behavioral answers.
4. **Python internals matter** — not just syntax. Know `asyncio`, GIL, concurrency, `mypy`, `pytest`, `FastAPI`.
5. **ETL/data pipeline experience is central** — this is the core of the Senior SWE role.
6. **Kafka + Airflow are nice-to-have but recurring** — study at least the concepts and use cases.
7. **Quant finance is a bonus, not a barrier** — JDs say "finance experience is a plus but not required". But knowing alpha, backtesting, and OHLCV data still helps.
8. **Observability matters** — OpenTelemetry, Grafana, ELK. They run production systems and care about diagnosing them.
9. **Open-source / public portfolio explicitly mentioned** — have something on GitHub.
10. **C++ is recurring across many roles** — even Python roles say "willing to learn C++". Basic C++ knowledge helps.

---

## 🌐 Research Findings (from WorldQuant Official Job Listings — Nov 2025)

> Sources: Scraped directly from [worldquant.com/career-listing](https://www.worldquant.com/career-listing/)

---

### 📋 Actual Job Description: Senior Software Engineer (Vietnam)

> **URL:** https://www.worldquant.com/career-listing/?id=4672066006  
> **Location:** Hanoi or Ho Chi Minh City, Vietnam

#### The Role (verbatim):
> _"Design, build, and operate large-scale data and ETL systems that power the firm's research and investment workflows. This is a high-autonomy role — you'll own critical systems end-to-end, make architectural decisions, and deliver solutions with minimal guidance."_

#### ✅ Hard Requirements (Must-Have):
- **8+ years** of professional software development experience
- **Python mastery** — language internals, performant & reliable code
- **System design** — distributed, scalable, fault-tolerant systems; event-driven architecture, caching, data partitioning
- **Data engineering** — ETL/ELT pipelines, batch + streaming, large-scale data processing
- **Database proficiency** — PostgreSQL/MySQL deep understanding, query optimization, strong SQL
- **API design** — REST / gRPC, clean and well-documented
- **Incident response** — root-cause analysis, production issue diagnosis, post-mortems
- **AI-agent readiness** — openness to LLM tools, AI coding agents as force multiplier

#### ⭐ Nice-to-Have (Will Make You Stand Out):
- Advanced Python internals: `asyncio`, `threading`, `multiprocessing`, `FastAPI`, `SQLAlchemy`, `pytest`, `mypy`
- Observability stack: metrics, structured logging, distributed tracing (OpenTelemetry, Grafana, ELK)
- DevOps: Docker, CI/CD (GitLab CI, Jenkins), Infrastructure-as-Code (Ansible, Terraform)
- Additional languages: **C++** (performance), **Scala/Spark** (distributed data), **Rust** (high-performance)
- Team leadership: sprints, code review, mentoring, stakeholder management
- Message queues & streaming: **Kafka**, Redis
- Data orchestration: **Apache Airflow**
- Frontend awareness: React, TypeScript
- **Financial services / quantitative finance background**
- Open-source contributions / public portfolio

---

### 📋 Actual Job Description: Senior Backend Engineer (Vietnam)

> **URL:** https://www.worldquant.com/career-listing/?id=4653484006  
> **Location:** Hanoi or Ho Chi Minh City, Vietnam

#### Hard Requirements:
- **5+ years** backend focus
- Data structures, algorithms, system design, software architecture
- Database proficiency — query optimization, schema design, data modeling
- Network protocols, API design, secure communication
- Full-stack understanding (frontend/backend interaction)
- **Production Python experience** (critical)
- Distributed systems design
- Containerization & orchestration
- Performance optimization & scalability

---

### 📋 Actual Job Description: Software Engineer (Vietnam — AI-Forward Team)

> **URL:** https://www.worldquant.com/career-listing/?id=4065713006  
> **Location:** Hanoi or Ho Chi Minh City, Vietnam

#### Key Highlights:
> _"This is an **AI-forward team**: LLMs and AI agents are part of our daily workflow — from writing and reviewing code, to automating operational toil, to building internal copilots and agentic tools."_

- **3–8 years** experience
- Python (preferred) or C++ on Linux/Unix
- Build data pipelines, computational frameworks, and quant strategy systems
- Work with Researchers and Quants as hands-on engineering partner
- Build and integrate **AI-powered tooling** — LLM agents, copilots, automation
- Experience with CI/CD, code version control
- Exceptional communication skills

---

### 📋 Key Themes Across ALL WorldQuant Tech Roles

| Theme | Frequency | Priority |
|---|---|---|
| Python (production-grade) | Every role | 🔴 Critical |
| Data structures & algorithms | Every role | 🔴 Critical |
| System design (distributed, scalable) | Every role | 🔴 Critical |
| Database / SQL proficiency | Every role | 🔴 Critical |
| ETL / Data pipelines | Senior roles | 🟠 High |
| API design (REST/gRPC) | Most roles | 🟠 High |
| AI/LLM tooling readiness | Newer roles | 🟠 High |
| Kafka / streaming | Senior roles | 🟡 Medium |
| Airflow / orchestration | Senior roles | 🟡 Medium |
| Docker / CI/CD / DevOps | Most roles | 🟡 Medium |
| C++ (performance) | Multiple roles | 🟡 Medium |
| Finance/quant domain knowledge | Nice to have | 🟢 Bonus |

---

### 🏢 Company Culture (from Job Descriptions)
- **"Intellectual horsepower first"** — they want smart thinkers, not checkbox checkers
- **High autonomy** — own systems end-to-end with minimal guidance
- **Academic + accountability** — curiosity meets delivery
- **AI-forward** — LLMs and agents are already part of daily engineering workflow
- **Cross-team collaboration** — work closely with Quants and Researchers
- **Continuous improvement mindset** — challenge conventional thinking

---

### 💰 Salary Benchmark (US reference from Trading Systems role)
> US Base Pay: **$150,000 – $250,000 USD** (Software Engineer - Trading Systems, NY)  
> Vietnam compensation is not published but is competitive for the local market with full benefits package.

---

### 🔗 Direct Job Listing URLs (Active as of Nov 2025)

| Role | Location | URL |
|---|---|---|
| Senior Software Engineer | Vietnam | https://www.worldquant.com/career-listing/?id=4672066006 |
| Senior Backend Engineer | Vietnam | https://www.worldquant.com/career-listing/?id=4653484006 |
| Software Engineer (AI team) | Vietnam | https://www.worldquant.com/career-listing/?id=4065713006 |
| Backend Engineer | Vietnam | https://www.worldquant.com/career-listing/?id=4665338006 |
| Full Stack Engineer | Vietnam | https://www.worldquant.com/career-listing/?id=4658486006 |
| Quantitative Developer | Vietnam | https://www.worldquant.com/career-listing/?id=4703213006 |
| Senior Python Engineer (AI) | Budapest | https://www.worldquant.com/career-listing/?id=4425930006 |
| Senior Python Software Engineer | Budapest | https://www.worldquant.com/career-listing/?id=4652057006 |
| Software Engineer - Trading Systems | New York | https://www.worldquant.com/career-listing/?id=4062126006 |

---

## ❓ Interview Question Bank (Collected from Internet)

> **Sources:** Glassdoor (archived 2015, 55 reviews), Wayback Machine  
> **Note:** Glassdoor/Reddit/Blind blocked headless browsers. Questions below are from archived Glassdoor + cross-referenced with role JDs. Most reviews were for Quant Researcher; SWE-specific ones are flagged.

---

### 🔁 WorldQuant Interview Process (Reported by Candidates)

```
Step 1: Recruiter Phone Screen (resume/skills fit, 20–30 min)
     ↓
Step 2: Online Test (Linux/Unix + SQL + one programming language — Python/C++)
         → "Hands-on experience required, theory alone won't pass"
     ↓
Step 3: Technical Phone Interview (half technical, half behavioral, 1 hr)
     ↓
Step 4: Onsite / Final Interview (reported as 4–9 hours, multiple interviewers)
         → Code on paper (whiteboard-style), no IDE
         → Series of algorithm + probability + system design sessions
```

> **Difficulty:** Rated 3.6/5 — **"Hard"** on Glassdoor  
> **Interview experience split:** 28% Positive, 37% Neutral, 34% Negative  
> **Time to complete:** 1 week – 4+ months (varies by role)

---

### 💻 Technical Questions — Algorithms & Data Structures

> Sourced from archived Glassdoor reviews (all roles, 2012–2015)

| # | Question | Category | Difficulty |
|---|---|---|---|
| 1 | Find the 3rd largest item in an array without sorting. Generalize to Nth largest. | Arrays / Heap | Medium |
| 2 | Given N numbers, form all subsets of N-1 elements. Compute the product of each subset **without using division**. Do it in O(N). | Arrays / Prefix Products | Hard |
| 3 | Find the 2nd largest element in an array with the **minimum number of comparisons**. | Arrays / Tournament | Hard |
| 4 | Josephus Problem — given N people in a circle, every Kth person is eliminated. Find the survivor. | Arrays / Math | Hard |
| 5 | Deep copy vs shallow copy — explain the difference and implement. | Python / Memory | Medium |
| 6 | Pointer vs reference in C++ — when to use each. | C++ | Medium |
| 7 | Global variable vs local variable — how to access/modify a global from a local scope in Python. | Python | Easy |
| 8 | What is the difference between Matlab and C++ in terms of data storage? | CS Fundamentals | Medium |
| 9 | Write a compilable, bug-free algorithm on paper (no IDE). | Any DSA | Hard |
| 10 | Write a function that returns the Nth Fibonacci number. Optimize it. | DP / Recursion | Easy–Medium |

---

### 🎲 Probability & Math Questions

> Common in Quant Researcher interviews; may appear in SWE interviews at WorldQuant

| # | Question | Type |
|---|---|---|
| 1 | You roll 3 dice (each 1–6). What is the probability that the **maximum** of the three rolls is exactly P? | Probability |
| 2 | Fair coin: what is the **expected number of throws** to get N consecutive heads? Find a recurrence relation between p(n) and p(n+1). | Probability / Recurrence |
| 3 | You have a biased coin where P(heads) = 51%. Create an event with exactly **P = 25%** using this coin. | Probability |
| 4 | There are 5 points in an equilateral triangle of side 1. Prove there exist 2 points with distance < 1/2. (Pigeonhole Principle) | Combinatorics / Proof |
| 5 | A calculator has all digit keys and arithmetic operators disabled. Only scientific functions (exp, log, sin, cos, arctan) work. It shows 0. Convert it to 2, then 3. | Math / Creativity |
| 6 | Given a random number from a **uniform distribution**, produce a random variable that is **normally distributed**. | Statistics / Simulation |
| 7 | Suppose expected coin tosses for N consecutive heads is p(n). Find the relationship between p(n) and p(n+1). | Probability / Recurrence |
| 8 | With your wildest imagination — give 3 things that can predict the stock price. | Domain / Creativity |

---

### 🐍 Python / Programming Language Questions

| # | Question | Topic |
|---|---|---|
| 1 | Explain the difference between `copy` and `deepcopy` in Python. When would each fail? | Python Internals |
| 2 | How does the GIL affect multithreading in Python? When should you use `multiprocessing` instead? | Concurrency |
| 3 | What are Python generators? How do they differ from iterators and lists? | Python Internals |
| 4 | Explain Python's memory management. What is reference counting? | Python Internals |
| 5 | What is a decorator? Implement a timing decorator. | Python |
| 6 | Explain `asyncio` — how does the event loop work? | Async / Concurrency |
| 7 | What is the difference between `@staticmethod`, `@classmethod`, and instance methods? | OOP |
| 8 | How would you profile a slow Python script? Walk me through the process. | Performance |
| 9 | What happens when you do `import module` in Python? How does the import system work? | Python Internals |
| 10 | Explain type hints in Python. What is the difference between `Protocol` and `ABC`? | Typing |

---

### 🌐 Network Knowledge Questions

> Covers the JD requirement: _"Solid grasp of network protocols, API design, and secure communication implementations"_

#### 🔌 Network Protocols

| # | Question | Topic |
|---|---|---|
| 1 | Walk me through what happens when you type `https://api.worldquant.com/data` in a browser — from DNS to TLS handshake to response. | HTTP / TLS / DNS |
| 2 | What is the difference between TCP and UDP? When would you choose UDP over TCP in a financial system? | Transport Layer |
| 3 | Explain the TCP 3-way handshake. What happens during connection teardown (4-way)? | TCP |
| 4 | What is HTTP/2 and how does it differ from HTTP/1.1? What is HTTP/3 (QUIC)? | HTTP |
| 5 | What is the difference between a reverse proxy and a load balancer? Give an example of each (e.g., Nginx, HAProxy). | Infrastructure |
| 6 | Explain WebSockets. How do they differ from long-polling and SSE (Server-Sent Events)? When would you use each? | Real-time Comms |
| 7 | What is a CDN and how does it work? When is it NOT useful? | Networking |
| 8 | Explain the OSI model in plain terms. Which layers matter most for a backend engineer? | Fundamentals |

#### 🔧 API Design

| # | Question | Topic |
|---|---|---|
| 1 | Design a RESTful API for serving computed financial signals. How do you handle versioning (`v1`, `v2`)? | REST Design |
| 2 | What is the difference between REST, GraphQL, and gRPC? When would you choose gRPC for internal services? | API Paradigms |
| 3 | What are idempotency and safety in REST? Which HTTP methods are idempotent? | REST Semantics |
| 4 | How do you handle API rate limiting? Describe token bucket vs leaky bucket algorithms. | Rate Limiting |
| 5 | Design a pagination strategy for an API returning millions of financial records. Compare offset vs cursor-based pagination. | API Design |
| 6 | How do you design backward-compatible APIs? What breaks backward compatibility? | Versioning |
| 7 | What is an API gateway? What responsibilities should it own vs the individual service? | Architecture |
| 8 | How would you design a webhook system where your service pushes real-time events to clients? | Event-Driven |

#### 🔒 Secure Communication

| # | Question | Topic |
|---|---|---|
| 1 | Explain TLS 1.3 handshake. What changed from TLS 1.2? Why does it matter for latency-sensitive systems? | TLS / Security |
| 2 | What is mTLS (Mutual TLS)? How does it differ from one-way TLS? When would you use it in a microservices system? | mTLS |
| 3 | Explain JWT (JSON Web Token). What are the risks of storing JWTs in `localStorage` vs `httpOnly` cookies? | Auth / Security |
| 4 | What is OAuth 2.0? Explain the difference between Authorization Code flow and Client Credentials flow. | OAuth |
| 5 | What is the difference between authentication and authorization? Give an example of each in a financial API. | Security Fundamentals |
| 6 | How do you prevent common API vulnerabilities: SQL injection, SSRF, IDOR, and excessive data exposure? | API Security |
| 7 | What is certificate pinning? When is it useful and when is it a maintenance burden? | TLS / Mobile |
| 8 | How do you securely store API keys and secrets in a production system? Compare env vars, Vault, AWS Secrets Manager. | Secrets Management |

#### 💡 Key Concepts Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NETWORK KNOWLEDGE MAP                            │
├─────────────────┬───────────────────────────────────────────────────┤
│ PROTOCOLS       │ TCP/IP, UDP, HTTP/1.1, HTTP/2, HTTP/3 (QUIC),     │
│                 │ WebSocket, DNS, TLS 1.2/1.3                        │
├─────────────────┼───────────────────────────────────────────────────┤
│ API DESIGN      │ REST (idempotency, versioning, pagination),        │
│                 │ gRPC (protobuf, streaming), GraphQL, WebHooks,     │
│                 │ Rate limiting (token bucket), API Gateway          │
├─────────────────┼───────────────────────────────────────────────────┤
│ SECURITY        │ TLS handshake, mTLS, JWT, OAuth 2.0,              │
│                 │ OWASP Top 10 (SSRF, IDOR, injection),             │
│                 │ Secrets management (Vault, AWS SSM)                │
└─────────────────┴───────────────────────────────────────────────────┘
```

#### 🔑 Must-Know Code Patterns

```python
# ── Secure HTTPS request with timeout + retry ──────────────────────
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def fetch_signal(url: str, api_key: str) -> dict:
    with httpx.Client(timeout=5.0, verify=True) as client:
        response = client.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        return response.json()

# ── gRPC client (stub pattern) ──────────────────────────────────────
import grpc
import signals_pb2_grpc, signals_pb2

with grpc.secure_channel(
    "signals.worldquant.internal:443",
    grpc.ssl_channel_credentials()
) as channel:
    stub = signals_pb2_grpc.SignalServiceStub(channel)
    response = stub.GetSignal(signals_pb2.SignalRequest(id="alpha_001"))

# ── JWT decode + verify (never trust without verification) ──────────
import jwt  # PyJWT

SECRET = "from-vault-not-hardcoded"
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
# Always verify: exp, iss, aud claims

# ── Rate limiter (token bucket) ─────────────────────────────────────
import time
from threading import Lock

class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate          # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()
        self._lock = Lock()

    def consume(self, n: int = 1) -> bool:
        with self._lock:
            now = time.monotonic()
            self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
            self.last = now
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False
```

#### 🗂️ WorldQuant-Specific Scenarios to Prepare

| Scenario | What to Discuss |
|---|---|
| Internal microservices communication | gRPC + mTLS, protobuf schemas, service mesh (Istio) |
| Serving financial signals via API | REST versioning, cursor pagination, rate limiting, caching (Redis) |
| Real-time market data ingestion | WebSocket / TCP streams, backpressure, Kafka consumers |
| Securing research platform APIs | OAuth 2.0 Client Credentials, API Gateway, JWT validation |
| Secret rotation in production | HashiCorp Vault dynamic secrets, AWS Secrets Manager, no hardcoded keys |

---

### 🗄️ Database / SQL Questions

| # | Question | Topic |
|---|---|---|
| 1 | What is the difference between `INNER JOIN`, `LEFT JOIN`, and `FULL OUTER JOIN`? | SQL Basics |
| 2 | How would you optimize a slow SQL query? Walk me through your process. | Query Optimization |
| 3 | Explain database indexes — when do they help? When can they hurt? | Indexing |
| 4 | What is the difference between OLTP and OLAP? | DB Design |
| 5 | Design a schema for storing financial tick data (OHLCV) at scale. | Schema Design |
| 6 | What is query plan analysis? How do you use EXPLAIN in PostgreSQL? | Performance |
| 7 | What is the difference between a clustered and non-clustered index? | Indexing |
| 8 | Write a SQL query to find the top 3 most traded stocks by volume in the last 7 days. | SQL |

---

### 🏗️ System Design Questions

> Derived from JD requirements — these are the most likely topics based on what the role actually involves

| # | Question | Focus Area |
|---|---|---|
| 1 | Design a **large-scale ETL pipeline** that ingests data from 10+ sources, normalizes it, and stores it for downstream research. | ETL / Data Engineering |
| 2 | Design a **real-time streaming system** for market data (millions of events/sec). How do you handle late events, deduplication, and backpressure? | Kafka / Streaming |
| 3 | Design a **backtesting engine** for quantitative trading strategies. How do you avoid look-ahead bias? | Quant / Data |
| 4 | Design a **distributed job scheduler** (like Apache Airflow). How do you handle failures, retries, and dependencies? | Orchestration |
| 5 | Design an **API service** that serves computed financial signals to downstream consumers. How do you handle caching, rate limiting, and versioning? | API / REST |
| 6 | You have a data pipeline that processes 1TB of daily market data. Walk me through how you'd architect the storage, processing, and serving layers. | Data Architecture |
| 7 | How would you add **observability** (logging, metrics, tracing) to an existing microservice? What tools would you use? | Observability |
| 8 | Design a **schema migration system** for a production database with no downtime. | DB / DevOps |

---

### 🖥️ Linux / DevOps Questions

> From the online test stage (Linux/Unix section is confirmed in multiple reviews)

| # | Question | Topic |
|---|---|---|
| 1 | How do you compress and decompress files in Linux? (`tar`, `gzip`, `zip`) | Linux |
| 2 | What is the difference between a process and a thread in Linux? | OS Fundamentals |
| 3 | How do you monitor CPU and memory usage in Linux? (`top`, `htop`, `ps`, `vmstat`) | Linux |
| 4 | Explain file permissions in Linux — what does `chmod 755` mean? | Linux |
| 5 | How do you find all files modified in the last 24 hours? | Linux / Shell |
| 6 | What is the difference between `fork()` and `exec()` in Unix? | OS / Systems |
| 7 | How would you kill a process that is hanging? | Linux |
| 8 | What is the difference between a hard link and a soft link? | Linux |
| 9 | Write a shell script that monitors a log file and alerts when it reaches 1GB. | Shell Scripting |
| 10 | Explain Docker — how does containerization differ from virtualization? | DevOps |

---

### 🧑‍💼 Behavioral Questions

> From archived Glassdoor — behavioral is "half the phone interview"

| # | Question | Senior-Level Angle |
|---|---|---|
| 1 | Tell me about a system you designed from scratch. What tradeoffs did you make? | Ownership / Architecture |
| 2 | Describe a time you handled a production incident. What was your process? | Incident Response |
| 3 | Tell me about a time you disagreed with a technical decision. What did you do? | Communication |
| 4 | How do you mentor junior engineers? Give a concrete example. | Leadership |
| 5 | Describe a project where you had ambiguous requirements. How did you proceed? | Autonomy (this is KEY at WQ) |
| 6 | Tell me about the most complex system you've worked on. How did you manage its complexity? | Technical Depth |
| 7 | Have you worked with AI tools (LLMs, Copilot, etc.) in your workflow? How? | AI-Forward Culture |
| 8 | How do you balance writing fast code vs correct code? Give an example. | Engineering Values |
| 9 | Tell me about a time you improved the performance of a system significantly. | Impact |
| 10 | What do you know about WorldQuant and what interests you about the role? | Culture Fit |

---

### 📊 Online Test Format (Confirmed from Glassdoor Reviews)

```
Section 1: Linux / Unix (command-line, file system, process management)
Section 2: SQL (queries, optimization, schema design)
Section 3: Programming Language — your choice (Python or C++)
           → "Hands-on experience required" — syntax alone won't pass
           → Expect to write actual working code, not pseudocode

Duration: ~2–4 hours total
Format: Practical coding + multiple choice + short answer
```

---

## 📊 Weekly Progress Tracker

| Week | Focus | LeetCode Solved | Mock Interviews | Key Win | Blocker |
|---|---|---|---|---|---|
| 1 | Python Advanced | | | | |
| 2 | Python + DSA start | | | | |
| 3 | DSA intensive | | | | |
| 4 | DSA intensive | | | | |
| 5 | System Design | | | | |
| 6 | System Design | | | | |
| 7 | Quant Finance | | | | |
| 8 | Mock Interviews | | | | |

---

## 💡 Key Insights & "Aha" Moments

> _Running list of important things you learn during prep_

- 
- 
- 

---

_Last updated: ____________
