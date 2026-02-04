---
layout: simple
title: "System Design: Skills Intelligence GraphRAG"
permalink: /system_design/design-skills-graphrag
---

# System Design: Skills Intelligence GraphRAG

## Combining Knowledge Graphs with Skills Ontology for Intelligent Talent Systems

> **Interview context**: This is a specialized system design combining GraphRAG (graph-based retrieval augmented generation) with HR/talent domain knowledge. It demonstrates how to build intelligent systems that understand relationships between skills, professions, and career paths.

---

## Table of Contents

1. [Problem Understanding](#1-problem-understanding)
2. [Skills Ontology Overview](#2-skills-ontology-overview)
3. [System Architecture](#3-system-architecture)
4. [Knowledge Graph Design](#4-knowledge-graph-design)
5. [GraphRAG Integration](#5-graphrag-integration)
6. [Use Cases & Query Patterns](#6-use-cases--query-patterns)
7. [Data Pipeline](#7-data-pipeline)
8. [Implementation Details](#8-implementation-details)
9. [Scalability & Performance](#9-scalability--performance)
10. [Advanced Features](#10-advanced-features)

---

## 1. Problem Understanding

### What Are We Building?

A **Skills Intelligence GraphRAG System** that combines:

1. **Skills Ontology** (Textkernel-style): Structured knowledge about skills, professions, and their relationships
2. **GraphRAG**: Graph-based retrieval for contextual, relationship-aware answers
3. **LLM Integration**: Natural language interface for complex talent queries

### Target Use Cases

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PRIMARY USE CASES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. TALENT MATCHING                                                 │
│     "Find candidates with Python skills who could transition       │
│      to Machine Learning Engineer roles"                           │
│                                                                     │
│  2. SKILLS GAP ANALYSIS                                            │
│     "What skills does John need to become a Data Scientist?"       │
│                                                                     │
│  3. CAREER PATH RECOMMENDATIONS                                    │
│     "What are potential career paths for a Frontend Developer?"    │
│                                                                     │
│  4. LEARNING RECOMMENDATIONS                                       │
│     "What courses should I take to move into Cloud Architecture?"  │
│                                                                     │
│  5. JOB DESCRIPTION GENERATION                                     │
│     "Generate required skills for a Senior DevOps Engineer"        │
│                                                                     │
│  6. WORKFORCE PLANNING                                             │
│     "What skills will our team need in 2 years given AI trends?"   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Why GraphRAG for Skills?

> **Interviewer might ask**: "Why not just use vector search?"

| Approach | Pros | Cons |
|----------|------|------|
| **Vector Search** | Semantic similarity, handles synonyms | Misses explicit relationships |
| **Keyword Search** | Fast, exact matches | No understanding of context |
| **GraphRAG** | Relationship-aware, traverses connections | More complex to build |

**GraphRAG advantage**: When asked "Python developer skills", it can traverse:
- Python → [related_to] → Data Analysis, ML, Web Dev
- Python Developer → [requires] → Python, Git, SQL
- Python → [prerequisite_for] → TensorFlow, Django

This relationship awareness enables career path analysis, skills gap detection, and intelligent recommendations that pure vector search cannot provide.

---

## 2. Skills Ontology Overview

### Textkernel Skills Intelligence Structure

Based on the Textkernel Ontology API:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SKILLS ONTOLOGY ENTITIES                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SKILLS                           PROFESSIONS                       │
│  ├── Skill ID                     ├── Profession ID                │
│  ├── Name (multi-language)        ├── Name (multi-language)        │
│  ├── Category                     ├── Industry/Domain              │
│  ├── Type (Hard/Soft/Tool)        ├── Seniority Levels            │
│  └── Certifications               └── Required Skills              │
│                                                                     │
│  RELATIONSHIPS                                                      │
│  ├── Profession → Skills (has_skill)                               │
│  ├── Skills → Professions (enables_profession)                     │
│  ├── Skill → Skill (similar_to, prerequisite_of, related_to)      │
│  └── Skill → Certification (validates)                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### API Endpoints (Textkernel Reference)

| Endpoint | Purpose |
|----------|---------|
| `/professions/suggest_skills` | Get skills for a profession |
| `/professions/compare_skills` | Compare skills between professions |
| `/skills/suggest_professions` | Get professions for skills |
| `/skills/compare_to_profession` | Compare skill set to profession |
| `/skills/suggest_skills` | Get similar/related skills |
| `/skills/similarity_score` | Calculate skill set similarity |

---

## 3. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SKILLS GRAPHRAG ARCHITECTURE                    │
└─────────────────────────────────────────────────────────────────────┘

                            ┌─────────────────┐
                            │   User Query    │
                            │  (Natural Lang) │
                            └────────┬────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         QUERY PROCESSOR                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Intent    │  │   Entity    │  │   Query     │                 │
│  │ Classifier  │  │  Extractor  │  │  Planner    │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
           ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
           │ Skills Graph  │ │ Vector Store  │ │ Document Store│
           │   (Neo4j)     │ │  (Embeddings) │ │  (Raw Data)   │
           └───────────────┘ └───────────────┘ └───────────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       CONTEXT ASSEMBLER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Graph     │  │   Vector    │  │  Hybrid     │                 │
│  │  Context    │  │   Context   │  │   Ranker    │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        LLM RESPONSE GENERATOR                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Prompt    │  │    LLM      │  │  Response   │                 │
│  │  Builder    │  │  (GPT-4)    │  │  Formatter  │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │    Response     │
                            │ (Structured +   │
                            │  Explanation)   │
                            └─────────────────┘
```

### Component Overview

| Component | Purpose | Technology |
|-----------|---------|------------|
| Query Processor | Parse & understand user queries | LLM + NER |
| Skills Graph | Store skills ontology | Neo4j / Amazon Neptune |
| Vector Store | Semantic similarity search | Pinecone / Weaviate |
| Document Store | Raw job descriptions, resumes | Elasticsearch / S3 |
| Context Assembler | Combine graph + vector results | Custom logic |
| LLM Generator | Generate natural language responses | GPT-4 / Claude |

---

## 4. Knowledge Graph Design

### Graph Schema

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SKILLS KNOWLEDGE GRAPH                         │
└─────────────────────────────────────────────────────────────────────┘

NODE TYPES:
═══════════

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     SKILL       │     │   PROFESSION    │     │    CATEGORY     │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id: string      │     │ id: string      │     │ id: string      │
│ name: string    │     │ name: string    │     │ name: string    │
│ type: enum      │     │ industry: string│     │ parent_id: str  │
│ description: str│     │ seniority: enum │     │ level: int      │
│ popularity: int │     │ avg_salary: int │     └─────────────────┘
│ growth_rate: flt│     │ demand_trend: st│
└─────────────────┘     └─────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  CERTIFICATION  │     │    INDUSTRY     │     │    LEARNING     │
├─────────────────┤     ├─────────────────┤     │    RESOURCE     │
│ id: string      │     │ id: string      │     ├─────────────────┤
│ name: string    │     │ name: string    │     │ id: string      │
│ provider: string│     │ growth: float   │     │ title: string   │
│ validity: int   │     │ size: int       │     │ type: enum      │
│ level: enum     │     └─────────────────┘     │ duration: int   │
└─────────────────┘                             │ provider: string│
                                                └─────────────────┘

RELATIONSHIP TYPES:
══════════════════

SKILL ──[SIMILAR_TO {score: 0.0-1.0}]──> SKILL
SKILL ──[PREREQUISITE_FOR]──> SKILL
SKILL ──[RELATED_TO {type: "complementary"|"alternative"}]──> SKILL
SKILL ──[BELONGS_TO]──> CATEGORY
SKILL ──[VALIDATED_BY]──> CERTIFICATION
SKILL ──[TAUGHT_BY]──> LEARNING_RESOURCE

PROFESSION ──[REQUIRES {importance: "must"|"nice"}]──> SKILL
PROFESSION ──[TRANSITIONS_TO {difficulty: 1-5}]──> PROFESSION
PROFESSION ──[BELONGS_TO]──> INDUSTRY
PROFESSION ──[SENIOR_VERSION_OF]──> PROFESSION

CATEGORY ──[PARENT_OF]──> CATEGORY
```

### Example Graph Data

```
                         ┌──────────────────┐
                         │    CATEGORY:     │
                         │   Programming    │
                         └────────┬─────────┘
                                  │ PARENT_OF
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │ Backend   │ │ Frontend  │ │   Data    │
            │Development│ │Development│ │ Science   │
            └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
                  │             │             │
                  ▼             ▼             ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │  Python   │ │JavaScript │ │  Python   │
            │  (Skill)  │ │  (Skill)  │ │  (Skill)  │
            └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
                  │             │             │
    ┌─────────────┼─────────────┼─────────────┤
    │             │             │             │
    ▼             ▼             ▼             ▼
┌────────┐  ┌────────┐   ┌────────┐    ┌────────┐
│ Django │  │ FastAPI│   │ React  │    │ Pandas │
│(Skill) │  │(Skill) │   │(Skill) │    │(Skill) │
└────────┘  └────────┘   └────────┘    └────────┘
    │
    │ VALIDATED_BY
    ▼
┌──────────────────┐
│   Django        │
│  Certification  │
└──────────────────┘
```

### Neo4j Schema (Cypher)

```cypher
// Create constraints
CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT profession_id IF NOT EXISTS FOR (p:Profession) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT category_id IF NOT EXISTS FOR (c:Category) REQUIRE c.id IS UNIQUE;

// Create indexes for search
CREATE INDEX skill_name IF NOT EXISTS FOR (s:Skill) ON (s.name);
CREATE INDEX profession_name IF NOT EXISTS FOR (p:Profession) ON (p.name);
CREATE FULLTEXT INDEX skill_search IF NOT EXISTS FOR (s:Skill) ON EACH [s.name, s.description];

// Example: Create skills
CREATE (python:Skill {
    id: 'skill_python',
    name: 'Python',
    type: 'hard_skill',
    description: 'General-purpose programming language',
    popularity: 95,
    growth_rate: 0.15
})

CREATE (ml:Skill {
    id: 'skill_ml',
    name: 'Machine Learning',
    type: 'hard_skill',
    description: 'Building systems that learn from data',
    popularity: 88,
    growth_rate: 0.25
})

// Example: Create relationships
MATCH (python:Skill {id: 'skill_python'})
MATCH (ml:Skill {id: 'skill_ml'})
CREATE (python)-[:PREREQUISITE_FOR]->(ml)
CREATE (python)-[:SIMILAR_TO {score: 0.7}]->(ml)

// Example: Profession with required skills
CREATE (ds:Profession {
    id: 'prof_data_scientist',
    name: 'Data Scientist',
    industry: 'Technology',
    seniority: 'mid',
    avg_salary: 120000
})

MATCH (ds:Profession {id: 'prof_data_scientist'})
MATCH (python:Skill {id: 'skill_python'})
MATCH (ml:Skill {id: 'skill_ml'})
CREATE (ds)-[:REQUIRES {importance: 'must', weight: 0.9}]->(python)
CREATE (ds)-[:REQUIRES {importance: 'must', weight: 0.95}]->(ml)
```

---

## 5. GraphRAG Integration

### Query Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GRAPHRAG QUERY PIPELINE                          │
└─────────────────────────────────────────────────────────────────────┘

User: "What skills should a Python developer learn to become a
       Machine Learning Engineer?"

STEP 1: INTENT CLASSIFICATION
─────────────────────────────
Intent: SKILLS_GAP_ANALYSIS
Entities:
  - Source Role: "Python Developer"
  - Target Role: "Machine Learning Engineer"

STEP 2: GRAPH QUERY GENERATION
─────────────────────────────
Query Plan:
  1. Find skills for "Python Developer"
  2. Find skills for "Machine Learning Engineer"
  3. Calculate skill gap (difference)
  4. Find learning paths for gap skills

Cypher Query:
```cypher
// Get source profession skills
MATCH (source:Profession {name: 'Python Developer'})-[:REQUIRES]->(s1:Skill)
WITH collect(s1) as sourceSkills

// Get target profession skills
MATCH (target:Profession {name: 'ML Engineer'})-[:REQUIRES]->(s2:Skill)
WITH sourceSkills, collect(s2) as targetSkills

// Find gap skills (in target but not in source)
WITH [s IN targetSkills WHERE NOT s IN sourceSkills] as gapSkills
UNWIND gapSkills as gap

// Find learning resources and prerequisites
OPTIONAL MATCH (gap)-[:TAUGHT_BY]->(resource:LearningResource)
OPTIONAL MATCH (prereq:Skill)-[:PREREQUISITE_FOR]->(gap)

RETURN gap, collect(DISTINCT resource) as resources,
       collect(DISTINCT prereq) as prerequisites
```

STEP 3: CONTEXT ASSEMBLY
─────────────────────────────
Graph Context:
  - Gap Skills: [TensorFlow, PyTorch, Deep Learning, MLOps]
  - Prerequisites: [Linear Algebra, Statistics, Python Advanced]
  - Learning Resources: [Coursera ML Course, Fast.ai, ...]

Vector Context (from job descriptions):
  - "ML Engineers typically need 2+ years of deep learning..."
  - "Key responsibilities include model deployment..."

STEP 4: LLM RESPONSE GENERATION
─────────────────────────────
Prompt: """
Based on the skills knowledge graph and job market data:

Current Role: Python Developer
Target Role: Machine Learning Engineer

Skills Gap Analysis:
{graph_context}

Additional Context:
{vector_context}

Generate a personalized learning roadmap with:
1. Priority skills to learn
2. Recommended learning order
3. Estimated time for each skill
4. Specific resources
"""

STEP 5: STRUCTURED RESPONSE
─────────────────────────────
{
  "summary": "To transition from Python Developer to ML Engineer...",
  "skills_gap": [...],
  "learning_roadmap": [...],
  "estimated_duration": "6-12 months",
  "confidence": 0.89
}
```

### Query Processing Flow

> **Interview context**: The core of GraphRAG is the query processing pipeline. Understand each step.

```
User Query: "What skills do I need to become a Machine Learning Engineer?"
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Step 1: INTENT CLASSIFICATION                                       │
│   Input: Natural language query                                     │
│   Output: SKILLS_GAP | CAREER_PATH | RECOMMENDATIONS | ...         │
│   Method: LLM prompt or fine-tuned classifier                      │
└─────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Step 2: ENTITY EXTRACTION                                           │
│   Input: Query text                                                 │
│   Output: {skills: [...], professions: [...], certifications: [...]}│
│   Method: NER or LLM extraction                                     │
└─────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Step 3: GRAPH QUERY GENERATION                                      │
│   Based on intent, generate appropriate Cypher query                │
│   - SKILLS_GAP → Compare profession skill sets                     │
│   - CAREER_PATH → Traverse TRANSITIONS_TO relationships            │
│   - RECOMMENDATIONS → Find related skills not in user's set        │
└─────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Step 4: CONTEXT ASSEMBLY                                            │
│   Combine: Graph results + Vector search results + User context     │
│   Format into prompt for LLM                                        │
└─────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Step 5: LLM RESPONSE GENERATION                                     │
│   LLM receives: Query + Intent + Graph Context + Vector Context    │
│   LLM produces: Structured answer citing graph relationships        │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Graph Queries

| Intent | What It Does | Graph Pattern |
|--------|--------------|---------------|
| **Skills Gap** | Compare skills between roles | `(CurrentRole)-[:REQUIRES]->() vs (TargetRole)-[:REQUIRES]->()` |
| **Career Path** | Find progression routes | `(Start)-[:TRANSITIONS_TO*1..4]->(End)` |
| **Recommendations** | Suggest related skills | `(UserSkill)-[:SIMILAR_TO|RELATED_TO]->(Recommended)` |
| **Profession Skills** | List required skills | `(Profession)-[:REQUIRES]->(Skill)` |

### Intent Classification

The system classifies queries into intents to choose the right graph traversal:

| Intent | Example Query | Graph Operation |
|--------|--------------|-----------------|
| `SKILLS_GAP` | "What skills do I need for X?" | Compare skill sets |
| `CAREER_PATH` | "How do I become X?" | Find path between roles |
| `SKILL_RECOMMENDATIONS` | "What should I learn next?" | Find related skills |
| `PROFESSION_SKILLS` | "What skills does X need?" | Get required skills |
| `SKILL_COMPARISON` | "How do X and Y compare?" | Similarity calculation |
| `MARKET_TRENDS` | "What skills are in demand?" | Aggregate trend data |
| `LEARNING_PATH` | "How do I learn X?" | Find prerequisites |

---

## 6. Use Cases & Query Patterns

### Use Case 1: Skills Gap Analysis

```
USER: "I'm a Python developer. What skills do I need to become a
       Machine Learning Engineer?"

GRAPH TRAVERSAL:
┌─────────────────┐     ┌─────────────────┐
│Python Developer │────>│   ML Engineer   │
└───────┬─────────┘     └────────┬────────┘
        │ REQUIRES               │ REQUIRES
        ▼                        ▼
   ┌─────────┐            ┌──────────────┐
   │ Python  │            │ TensorFlow   │ ← GAP
   │ Git     │            │ PyTorch      │ ← GAP
   │ SQL     │            │ Deep Learning│ ← GAP
   │ REST API│            │ MLOps        │ ← GAP
   └─────────┘            │ Python       │ ← HAVE
                          │ Statistics   │ ← GAP
                          └──────────────┘

RESPONSE:
{
  "skills_gap": [
    {"skill": "TensorFlow", "priority": "high", "learning_time": "2 months"},
    {"skill": "Deep Learning", "priority": "high", "learning_time": "3 months"},
    {"skill": "PyTorch", "priority": "medium", "learning_time": "2 months"},
    {"skill": "Statistics", "priority": "high", "learning_time": "1 month"}
  ],
  "recommended_order": ["Statistics", "Deep Learning", "TensorFlow", "PyTorch"],
  "total_time": "6-9 months"
}
```

### Use Case 2: Career Path Discovery

```
USER: "What are career paths for a Frontend Developer?"

GRAPH TRAVERSAL:
                    ┌─────────────────────┐
                    │ Frontend Developer  │
                    └──────────┬──────────┘
                               │ TRANSITIONS_TO
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Senior Frontend │  │ Full Stack Dev  │  │   UX Engineer   │
│   Developer     │  │                 │  │                 │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Frontend Arch   │  │  Tech Lead      │  │ Design Systems  │
└────────┬────────┘  └────────┬────────┘  │    Lead         │
         │                    │           └─────────────────┘
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│ Engineering     │  │    CTO          │
│   Manager       │  │                 │
└─────────────────┘  └─────────────────┘

RESPONSE:
{
  "career_paths": [
    {
      "path": ["Frontend Dev", "Senior Frontend", "Frontend Architect"],
      "focus": "Technical depth",
      "difficulty": "medium"
    },
    {
      "path": ["Frontend Dev", "Full Stack", "Tech Lead", "CTO"],
      "focus": "Leadership",
      "difficulty": "hard"
    },
    {
      "path": ["Frontend Dev", "UX Engineer", "Design Systems Lead"],
      "focus": "Design + Code",
      "difficulty": "medium"
    }
  ]
}
```

### Use Case 3: Skill Similarity & Recommendations

```
USER: "I know Python and SQL. What related skills should I learn?"

GRAPH TRAVERSAL:
         ┌────────────────────────────────────┐
         │         User's Skills              │
         │      [Python, SQL]                 │
         └──────────────┬─────────────────────┘
                        │ SIMILAR_TO / RELATED_TO
    ┌───────────────────┼───────────────────────┐
    ▼                   ▼                       ▼
┌────────┐        ┌──────────┐           ┌──────────┐
│  R     │        │  Pandas  │           │PostgreSQL│
│(0.65)  │        │  (0.85)  │           │  (0.90)  │
└────────┘        └──────────┘           └──────────┘
    │                  │                      │
    ▼                  ▼                      ▼
┌────────┐        ┌──────────┐           ┌──────────┐
│Statistics│       │  NumPy   │           │  NoSQL   │
│ (0.70)  │       │  (0.82)  │           │  (0.75)  │
└─────────┘       └──────────┘           └──────────┘

RESPONSE:
{
  "recommendations": [
    {"skill": "Pandas", "similarity": 0.85, "reason": "Essential for Python data work"},
    {"skill": "PostgreSQL", "similarity": 0.90, "reason": "Advanced SQL database"},
    {"skill": "NumPy", "similarity": 0.82, "reason": "Foundation for data science"},
    {"skill": "Statistics", "similarity": 0.70, "reason": "Complements data skills"}
  ]
}
```

### Use Case 4: Job Description Generation

```
USER: "Generate required skills for a Senior DevOps Engineer position"

GRAPH QUERY:
MATCH (p:Profession {name: 'Senior DevOps Engineer'})-[r:REQUIRES]->(s:Skill)
RETURN s.name, r.importance, r.weight
ORDER BY r.weight DESC

RESPONSE:
{
  "required_skills": {
    "must_have": [
      "Kubernetes", "Docker", "AWS/GCP/Azure",
      "CI/CD", "Linux", "Terraform"
    ],
    "nice_to_have": [
      "Python/Go", "Prometheus", "GitOps",
      "Security", "Networking"
    ]
  },
  "generated_description": "We're looking for a Senior DevOps Engineer..."
}
```

---

## 7. Data Pipeline

### Data Ingestion Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA INGESTION PIPELINE                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐
│ Textkernel  │    │ Job Boards  │    │   Resumes   │    │ Courses  │
│  Skills API │    │(Indeed,etc) │    │  (User Data)│    │(Coursera)│
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └────┬─────┘
       │                  │                  │                 │
       ▼                  ▼                  ▼                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA COLLECTORS                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  API Client │  │  Scraper    │  │  File Parser│                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA PROCESSING                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Entity    │  │  Relation   │  │   Data      │                 │
│  │ Extraction  │  │ Extraction  │  │ Validation  │                 │
│  │   (LLM)     │  │   (LLM)     │  │             │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GRAPH CONSTRUCTION                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Entity    │  │  Relation   │  │   Graph     │                 │
│  │  Resolver   │  │  Merger     │  │  Writer     │                 │
│  │(Dedup/Match)│  │             │  │  (Neo4j)    │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Skills Knowledge│
                    │     Graph       │
                    └─────────────────┘
```

### Entity Extraction Pipeline

> **Interview context**: The entity extraction pipeline converts unstructured data (job descriptions, resumes) into structured graph data. This is where LLMs add significant value.

**Key extraction steps:**

1. **Job Description Processing**
   - Extract job title, required skills, responsibilities
   - Classify skill importance ("must-have" vs "nice-to-have")
   - Identify certification requirements and experience levels

2. **Resume Processing**
   - Extract skills with proficiency levels
   - Map experience to skills used
   - Identify certifications and education

3. **Entity Resolution**
   - Match extracted skills to canonical taxonomy (Textkernel)
   - Handle synonyms: "JS" → "JavaScript", "ML" → "Machine Learning"
   - Merge duplicates with confidence scoring

4. **Similarity Computation**
   - Co-occurrence analysis: skills appearing together in job postings
   - Jaccard similarity for relationship strength
   - Threshold filtering (similarity > 0.3) to avoid noise

> **Interviewer might ask**: "Why use LLMs for extraction instead of NER models?"
>
> LLMs handle the nuance of skill descriptions better. "3+ years Python experience" vs "Python preferred" encode different requirements. NER would need extensive training data to capture these distinctions.

---

## 8. Scalability & Performance

> **Interview context**: At scale, the main bottlenecks are graph queries, LLM calls, and entity extraction. Each requires different optimization strategies.

### Caching Strategy

**Multi-level caching** is essential for production GraphRAG systems:

| Cache Level | What to Cache | TTL | Why |
|-------------|---------------|-----|-----|
| **L1 (In-memory)** | Hot queries | Session | Instant access for repeated queries |
| **L2 (Redis)** | Graph query results | 1 hour | Graph data changes slowly |
| **L3 (Redis)** | LLM responses | 24 hours | Expensive to regenerate |
| **L4 (Persistent)** | Entity extractions | 7 days | Job descriptions don't change |

**Cache key strategy**: Hash the query + context to generate deterministic keys. Normalize queries before hashing to improve cache hit rates.

> **Interviewer might ask**: "What about cache invalidation?"
>
> For skills data, time-based expiration usually suffices—the graph updates gradually. For user-specific queries (like skills gap analysis), we use user_id + timestamp in the cache key to ensure fresh results after profile updates.

### Query Optimization

**Key optimization strategies:**

1. **Indexing**: Composite indexes on frequently queried relationship properties
2. **Clustering**: Pre-compute skill clusters using community detection (Louvain algorithm)
3. **Caching hot paths**: Career path queries that traverse multiple hops

> **Interviewer might ask**: "How do you optimize graph queries at scale?"
>
> Three levels: (1) Proper indexing on node/relationship properties, (2) Pre-computed aggregations for expensive traversals, (3) Query result caching for repeated patterns. The goal is sub-100ms response times even for complex multi-hop queries.

---

## 9. Advanced Features

### 9.1 Trend Analysis

**Growth rate computation** identifies rising and declining skills:

1. Compare skill mentions in recent vs older job postings (30-day vs 90-day windows)
2. Classify as "rising" (>20% growth), "declining" (<-20%), or "stable"
3. Store growth_rate and trend as node properties for fast filtering

**Use cases:**
- Surface "Skills to Watch" in career planning
- Alert L&D teams about emerging skill gaps
- Inform curriculum development priorities

### 9.2 Personalized Recommendations

**Recommendation scoring formula:**

```
score = (goal_relevance × 0.4) + (growth_rate × 0.3) + (popularity × 0.3)
```

| Factor | Weight | Why |
|--------|--------|-----|
| **Goal relevance** | 40% | Skills that lead to user's career goals |
| **Growth rate** | 30% | Skills with increasing market demand |
| **Popularity** | 30% | Skills with established job market presence |

> **Interviewer might ask**: "How do you personalize recommendations?"
>
> We build a user context from their profile (current skills, experience, goals, interests) and use it to filter and rank the graph traversal results. The LLM then explains WHY each recommendation matters for this specific user.

### 9.3 Natural Language to Cypher (NL2Cypher)

**The challenge**: Convert questions like "What skills should I learn for machine learning?" into graph queries.

**Approach:**
1. Provide graph schema to LLM as context
2. Use few-shot examples of NL → Cypher conversions
3. Validate generated Cypher syntax before execution
4. Fall back to semantic search if Cypher generation fails

**Schema provided to LLM:**
- Node types: Skill, Profession, Category, Certification, LearningResource
- Relationships: REQUIRES, SIMILAR_TO, PREREQUISITE_FOR, BELONGS_TO, VALIDATED_BY, TAUGHT_BY, TRANSITIONS_TO

> **Interviewer might ask**: "What if the LLM generates invalid Cypher?"
>
> We validate syntax before execution and have fallback strategies: (1) retry with rephrased prompt, (2) fall back to predefined query templates, (3) use semantic search as last resort. Always return something useful rather than failing.

---

## Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│              SKILLS GRAPHRAG SYSTEM SUMMARY                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CORE COMPONENTS                                                    │
│  ├── Skills Knowledge Graph (Neo4j)                                │
│  ├── Entity Extraction Pipeline (LLM-based)                        │
│  ├── GraphRAG Query Engine                                         │
│  ├── Response Generator (GPT-4)                                    │
│  └── Caching Layer (Redis)                                         │
│                                                                     │
│  KEY FEATURES                                                       │
│  ├── Natural language queries about skills                         │
│  ├── Skills gap analysis                                           │
│  ├── Career path recommendations                                   │
│  ├── Personalized skill recommendations                            │
│  ├── Trend analysis and forecasting                               │
│  └── Integration with Textkernel ontology                          │
│                                                                     │
│  DATA SOURCES                                                       │
│  ├── Textkernel Skills Intelligence API                           │
│  ├── Job descriptions (scraped/API)                               │
│  ├── Resumes/CVs                                                   │
│  └── Learning platforms (Coursera, etc.)                          │
│                                                                     │
│  USE CASES                                                          │
│  ├── HR/Recruiting: Candidate matching                             │
│  ├── L&D: Learning recommendations                                 │
│  ├── Workforce Planning: Skill forecasting                        │
│  └── Career Development: Path planning                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Interview Tips

### Key Points to Emphasize

```
1. WHY GRAPH FOR SKILLS?
   "Skills have relationships - prerequisites, similarity, career paths.
    A graph captures these explicitly while vector search only finds
    semantic similarity."

2. GRAPHRAG ADVANTAGES
   "We combine graph traversal (explicit relationships) with vector
    search (semantic similarity) for best of both worlds."

3. DOMAIN-SPECIFIC MODELING
   "Skills ontology is different from general knowledge graphs.
    It has specific relationships: REQUIRES, TRANSITIONS_TO,
    PREREQUISITE_FOR, SIMILAR_TO."
```

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "Why not just vector search?" | Misses explicit relationships, can't traverse career paths |
| "How do you keep the graph updated?" | Data pipeline from job boards, manual curation, trend analysis |
| "How do you handle synonyms?" | Multiple labels per skill, similarity relationships, LLM normalization |
| "Scalability concerns?" | Graph database scaling (Neo4j clusters), caching hot paths |
| "How accurate are recommendations?" | Feedback loops, A/B testing, domain expert validation |

### Trade-offs to Discuss

| Decision | Option A | Option B |
|----------|----------|----------|
| **Graph DB** | Neo4j (mature, Cypher) | Amazon Neptune (managed, SPARQL) |
| **Embeddings** | Pre-computed (fast) | On-demand (flexible) |
| **Entity extraction** | LLM (flexible) | NER model (faster) |
| **Response generation** | LLM (natural) | Template-based (predictable) |

---

## References

- [Textkernel Skills Intelligence API](https://developer.textkernel.com/SkillsIntelligence/master/ontology/)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/)
- [LangChain Graph QA](https://python.langchain.com/docs/use_cases/graph/)
