---
layout: simple
title: "Low Level Design"
permalink: /low_level_design
---

# Low Level Design

A comprehensive guide to Low Level Design (LLD) interview preparation — covering OOP fundamentals, design patterns, UML diagrams, concurrency, and 33 real-world LLD interview problems with implementations.

> **Source**: Content curated from [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design) by Ashish Pratap Singh.

---

## How to Use This Guide

LLD interviews test your ability to design **class-level architectures**:

1. **Master OOP fundamentals first** — They're the building blocks for every LLD question
2. **Learn design patterns** — Recognize which pattern solves which problem
3. **Practice UML diagrams** — Be able to sketch class diagrams quickly on a whiteboard
4. **Solve LLD problems** — Start with Easy, progress to Hard. For each problem, try designing before looking at the solution

> **Tip**: In LLD interviews, focus on identifying the right **entities**, **relationships**, and **design patterns**. A clean class hierarchy beats clever code.

---

## OOP Fundamentals

Core object-oriented programming concepts you must know before tackling any LLD problem.

| Concept | Description |
|---------|-------------|
| [Classes and Objects](https://algomaster.io/learn/lld/classes-and-objects) | Blueprints and instances — the foundation of OOP |
| [Enums](https://algomaster.io/learn/lld/enums) | Type-safe constants for fixed sets of values |
| [Interfaces](https://algomaster.io/learn/lld/interfaces) | Contracts that define behavior without implementation |
| [Encapsulation](https://algomaster.io/learn/lld/encapsulation) | Bundling data with methods, controlling access |
| [Abstraction](https://algomaster.io/learn/lld/abstraction) | Hiding complexity, exposing only essentials |
| [Inheritance](https://algomaster.io/learn/lld/inheritance) | Code reuse through parent-child class hierarchies |
| [Polymorphism](https://algomaster.io/learn/lld/polymorphism) | One interface, many implementations |

### Class Relationships

| Relationship | Description |
|-------------|-------------|
| [Association](https://algomaster.io/learn/lld/association) | Objects that know about each other (has-a, loosely) |
| [Aggregation](https://algomaster.io/learn/lld/aggregation) | Whole-part where parts can exist independently |
| [Composition](https://algomaster.io/learn/lld/composition) | Whole-part where parts cannot exist without the whole |
| [Dependency](https://algomaster.io/learn/lld/dependency) | One class uses another temporarily |

---

## Design Principles

| Principle | Description |
|-----------|-------------|
| [DRY (Don't Repeat Yourself)](https://algomaster.io/learn/lld/dry) | Every piece of knowledge should have a single representation |
| [YAGNI (You Aren't Gonna Need It)](https://algomaster.io/learn/lld/yagni) | Don't build what you don't need yet |
| [KISS (Keep It Simple, Stupid)](https://algomaster.io/learn/lld/kiss) | Simplicity should be a key goal in design |
| [SOLID Principles with Pictures](https://medium.com/backticks-tildes/the-s-o-l-i-d-principles-in-pictures-b34ce2f1e898) | Visual guide to S.O.L.I.D. |
| [SOLID Principles with Code](https://blog.algomaster.io/p/solid-principles-explained-with-code) | Code examples for each SOLID principle |

---

## Design Patterns

The 23 Gang of Four (GoF) patterns organized by intent.

### Creational Patterns

> *How objects are created — abstracting the instantiation process.*

| Pattern | Key Idea |
|---------|----------|
| [Singleton](https://algomaster.io/learn/lld/singleton) | Exactly one instance, global access point |
| [Factory Method](https://algomaster.io/learn/lld/factory-method) | Defer instantiation to subclasses |
| [Abstract Factory](https://algomaster.io/learn/lld/abstract-factory) | Create families of related objects |
| [Builder](https://algomaster.io/learn/lld/builder) | Construct complex objects step by step |
| [Prototype](https://algomaster.io/learn/lld/prototype) | Clone existing objects instead of creating new |

### Structural Patterns

> *How classes and objects are composed to form larger structures.*

| Pattern | Key Idea |
|---------|----------|
| [Adapter](https://algomaster.io/learn/lld/adapter) | Convert one interface to another |
| [Bridge](https://algomaster.io/learn/lld/bridge) | Separate abstraction from implementation |
| [Composite](https://algomaster.io/learn/lld/composite) | Treat individual objects and compositions uniformly |
| [Decorator](https://algomaster.io/learn/lld/decorator) | Add responsibilities dynamically |
| [Facade](https://algomaster.io/learn/lld/facade) | Simplified interface to a complex subsystem |
| [Flyweight](https://algomaster.io/learn/lld/flyweight) | Share objects to support large numbers efficiently |
| [Proxy](https://algomaster.io/learn/lld/proxy) | Placeholder that controls access to another object |

### Behavioral Patterns

> *How objects interact and distribute responsibility.*

| Pattern | Key Idea |
|---------|----------|
| [Iterator](https://algomaster.io/learn/lld/iterator) | Sequential access without exposing internals |
| [Observer](https://algomaster.io/learn/lld/observer) | Notify dependents when state changes |
| [Strategy](https://algomaster.io/learn/lld/strategy) | Swap algorithms at runtime |
| [Command](https://algomaster.io/learn/lld/command) | Encapsulate requests as objects |
| [State](https://algomaster.io/learn/lld/state) | Alter behavior when internal state changes |
| [Template Method](https://algomaster.io/learn/lld/template-method) | Define algorithm skeleton, let subclasses fill steps |
| [Visitor](https://algomaster.io/learn/lld/visitor) | Add operations without modifying classes |
| [Mediator](https://algomaster.io/learn/lld/mediator) | Centralize complex communications |
| [Memento](https://algomaster.io/learn/lld/memento) | Capture and restore object state |
| [Chain of Responsibility](https://algomaster.io/learn/lld/chain-of-responsibility) | Pass request along a chain of handlers |

---

## UML Diagrams

| Diagram | Purpose |
|---------|---------|
| [Class Diagram](https://algomaster.io/learn/lld/class-diagram) | Structure of classes, attributes, methods, and relationships |
| [Use Case Diagram](https://algomaster.io/learn/lld/use-case-diagram) | System functionality from the user's perspective |
| [Sequence Diagram](https://algomaster.io/learn/lld/sequence-diagram) | Interaction between objects over time |
| [Activity Diagram](https://algomaster.io/learn/lld/activity-diagram) | Workflow and control flow of a system |
| [State Machine Diagram](https://algomaster.io/learn/lld/state-machine-diagram) | State transitions of an object |

---

## LLD Interview Problems

33 problems organized by difficulty. Each links to a problem description with requirements, class diagram, and multi-language implementations.

### Easy (7 problems)

| # | Problem | Key Concepts |
|---|---------|-------------|
| 1 | [Design Parking Lot](/cses-analyses/low_level_design/parking-lot) | Singleton, Factory, Observer |
| 2 | [Design Stack Overflow](/cses-analyses/low_level_design/stack-overflow) | Singleton, Composite, Facade |
| 3 | [Design a Vending Machine](/cses-analyses/low_level_design/vending-machine) | State Pattern, Singleton |
| 4 | [Design Logging Framework](/cses-analyses/low_level_design/logging-framework) | Singleton, Strategy |
| 5 | [Design Traffic Signal Control System](/cses-analyses/low_level_design/traffic-signal) | Singleton, Observer |
| 6 | [Design Coffee Vending Machine](/cses-analyses/low_level_design/coffee-vending-machine) | Singleton |
| 7 | [Design a Task Management System](/cses-analyses/low_level_design/task-management-system) | Singleton |

### Medium (15 problems)

| # | Problem | Key Concepts |
|---|---------|-------------|
| 1 | [Design ATM](/cses-analyses/low_level_design/atm) | Template Method, Facade |
| 2 | [Design LinkedIn](/cses-analyses/low_level_design/linkedin) | Singleton |
| 3 | [Design LRU Cache](/cses-analyses/low_level_design/lru-cache) | HashMap + Doubly Linked List |
| 4 | [Design Tic Tac Toe Game](/cses-analyses/low_level_design/tic-tac-toe) | OO Decomposition |
| 5 | [Design Pub Sub System](/cses-analyses/low_level_design/pub-sub-system) | Observer |
| 6 | [Design an Elevator System](/cses-analyses/low_level_design/elevator-system) | Controller, Concurrency |
| 7 | [Design Car Rental System](/cses-analyses/low_level_design/car-rental-system) | Singleton, Strategy |
| 8 | [Design an Online Auction System](/cses-analyses/low_level_design/online-auction-system) | Singleton |
| 9 | [Design Hotel Management System](/cses-analyses/low_level_design/hotel-management-system) | Singleton, Strategy |
| 10 | [Design a Digital Wallet Service](/cses-analyses/low_level_design/digital-wallet-service) | Singleton, Polymorphism |
| 11 | [Design Airline Management System](/cses-analyses/low_level_design/airline-management-system) | Singleton |
| 12 | [Design a Library Management System](/cses-analyses/low_level_design/library-management-system) | Singleton |
| 13 | [Design a Social Network like Facebook](/cses-analyses/low_level_design/social-networking-service) | Singleton |
| 14 | [Design Restaurant Management System](/cses-analyses/low_level_design/restaurant-management-system) | Singleton |
| 15 | [Design a Concert Ticket Booking System](/cses-analyses/low_level_design/concert-ticket-booking-system) | Singleton |

### Hard (11 problems)

| # | Problem | Key Concepts |
|---|---------|-------------|
| 1 | [Design CricInfo](/cses-analyses/low_level_design/cricinfo) | Singleton (multi-service) |
| 2 | [Design Splitwise](/cses-analyses/low_level_design/splitwise) | Singleton, Polymorphism |
| 3 | [Design Chess Game](/cses-analyses/low_level_design/chess-game) | Strategy, Polymorphism |
| 4 | [Design a Snake and Ladder Game](/cses-analyses/low_level_design/snake-and-ladder) | Singleton, Threading |
| 5 | [Design Ride-Sharing Service like Uber](/cses-analyses/low_level_design/ride-sharing-service) | Singleton |
| 6 | [Design Course Registration System](/cses-analyses/low_level_design/course-registration-system) | Singleton, Observer |
| 7 | [Design Movie Ticket Booking System](/cses-analyses/low_level_design/movie-ticket-booking-system) | Singleton |
| 8 | [Design Online Shopping System like Amazon](/cses-analyses/low_level_design/online-shopping-service) | Singleton |
| 9 | [Design Online Stock Brokerage System](/cses-analyses/low_level_design/online-stock-brokerage-system) | Singleton, Polymorphism |
| 10 | [Design Music Streaming Service like Spotify](/cses-analyses/low_level_design/music-streaming-service) | Singleton (multi-service) |
| 11 | [Design Online Food Delivery Service like Swiggy](/cses-analyses/low_level_design/food-delivery-service) | Singleton |

---

## Concurrency & Multi-threading

### Concepts

#### Concurrency 101

| Topic | Description |
|-------|-------------|
| [Introduction to Concurrency](https://algomaster.io/learn/concurrency-interview/introduction-to-concurrency) | Why concurrency matters in modern systems |
| [Concurrency vs Parallelism](https://algomaster.io/learn/concurrency-interview/concurrency-vs-parallelism) | Interleaving vs simultaneous execution |
| [Processes vs Threads](https://algomaster.io/learn/concurrency-interview/processes-vs-threads) | Isolation vs shared memory trade-offs |
| [Thread Lifecycle and States](https://algomaster.io/learn/concurrency-interview/thread-lifecycle-and-states) | New, Runnable, Blocked, Waiting, Terminated |
| [Race Conditions and Critical Sections](https://algomaster.io/learn/concurrency-interview/race-conditions-and-critical-sections) | When shared state goes wrong |

#### Synchronization Primitives

| Primitive | Description |
|-----------|-------------|
| [Mutex](https://algomaster.io/learn/concurrency-interview/mutex) | Mutual exclusion — one thread at a time |
| [Semaphores](https://algomaster.io/learn/concurrency-interview/semaphores) | Counting-based access control |
| [Condition Variables](https://algomaster.io/learn/concurrency-interview/condition-variables) | Wait for a condition to become true |
| [Coarse vs Fine-grained Locking](https://algomaster.io/learn/concurrency-interview/coarse-vs-fine-grained-locking) | Lock granularity trade-offs |
| [Reentrant Locks](https://algomaster.io/learn/concurrency-interview/reentrant-locks) | Locks a thread can acquire multiple times |
| [Try-Lock and Timed Locking](https://algomaster.io/learn/concurrency-interview/try-lock-and-timed-locking) | Non-blocking lock acquisition |
| [Compare-and-Swap (CAS)](https://algomaster.io/learn/concurrency-interview/compare-and-swap) | Lock-free atomic operation |

#### Concurrency Challenges

| Challenge | Description |
|-----------|-------------|
| [Deadlock](https://algomaster.io/learn/concurrency-interview/deadlock) | Circular wait causing permanent blocking |
| [Livelock](https://algomaster.io/learn/concurrency-interview/livelock) | Threads keep changing state but make no progress |

#### Concurrency Patterns

| Pattern | Description |
|---------|-------------|
| [Signaling Pattern](https://algomaster.io/learn/concurrency-interview/signaling-pattern) | One thread notifies another |
| [Thread Pool Pattern](https://algomaster.io/learn/concurrency-interview/thread-pool-pattern) | Reuse a fixed set of threads |
| [Producer-Consumer Pattern](https://algomaster.io/learn/concurrency-interview/producer-consumer-pattern) | Decouple production from consumption |
| [Reader-Writer Pattern](https://algomaster.io/learn/concurrency-interview/reader-writer-pattern) | Multiple readers, exclusive writers |

### Concurrency Problems

| Problem | Description |
|---------|-------------|
| [Print FooBar Alternately](https://algomaster.io/learn/concurrency-interview/print-foobar-alternately) | Coordinate two threads to alternate output |
| [Print Zero Even Odd](https://algomaster.io/learn/concurrency-interview/print-zero-even-odd) | Three threads printing in sequence |
| [Fizz Buzz Multithreaded](https://algomaster.io/learn/concurrency-interview/fizz-buzz-multithreaded) | Four threads coordinating FizzBuzz |
| [Building H2O Molecule](https://algomaster.io/learn/concurrency-interview/building-h2o) | Barrier synchronization |
| [Design Thread-Safe Cache with TTL](https://algomaster.io/learn/concurrency-interview/design-thread-safe-cache-with-ttl) | Concurrent access + expiration |
| [Design Concurrent HashMap](https://algomaster.io/learn/concurrency-interview/design-concurrent-hashmap) | Segment locking, CAS |
| [Design Thread-Safe Blocking Queue](https://algomaster.io/learn/concurrency-interview/design-thread-safe-blocking-queue) | Producer-consumer foundation |
| [Design Concurrent Bloom Filter](https://algomaster.io/learn/concurrency-interview/design-concurrent-bloom-filter) | Probabilistic data structure + concurrency |
| [Multi-threaded Merge Sort](https://algomaster.io/learn/concurrency-interview/multi-threaded-merge-sort) | Divide-and-conquer parallelism |

---

## LLD Interview Framework

### Step-by-Step Approach (45 min)

```
0-5 min:   CLARIFY REQUIREMENTS
           - What are the core use cases?
           - What entities are involved?
           - Any constraints (single/multi-threaded, scale)?

5-15 min:  IDENTIFY CLASSES & RELATIONSHIPS
           - List the main entities (nouns = classes)
           - Identify actions (verbs = methods)
           - Determine relationships (is-a, has-a, uses)

15-35 min: DESIGN & IMPLEMENT
           - Draw UML class diagram
           - Apply relevant design patterns
           - Write key class interfaces and methods
           - Handle edge cases

35-45 min: REVIEW & DISCUSS
           - Walk through a use case end-to-end
           - Discuss extensibility ("What if we add X?")
           - Address concurrency if relevant
```

### Common Patterns in LLD Interviews

| When you see... | Think about... |
|----------------|----------------|
| Multiple states for an object | **State Pattern** |
| Need to notify multiple objects | **Observer Pattern** |
| Multiple algorithms for same task | **Strategy Pattern** |
| Complex object construction | **Builder Pattern** |
| Only one instance needed | **Singleton Pattern** |
| Pass request through handlers | **Chain of Responsibility** |
| Undo/redo functionality | **Command + Memento** |
| Treat group same as individual | **Composite Pattern** |

---

## Resources

- [awesome-low-level-design (GitHub)](https://github.com/ashishps1/awesome-low-level-design) — Source repository with implementations in Java, Python, C++, C#, Go, TypeScript
- [AlgoMaster LLD Course](https://algomaster.io/learn/lld/course-introduction) — Comprehensive LLD interview course
- [AlgoMaster Concurrency Course](https://algomaster.io/learn/concurrency-interview) — Concurrency & multi-threading course
- [Head First Design Patterns](https://www.amazon.in/dp/9385889753) — Visual guide to design patterns
- [Clean Code](https://www.amazon.in/dp/B001GSTOAM) — Writing maintainable code
- [Refactoring](https://www.amazon.in/dp/0134757599) — Improving existing code design
