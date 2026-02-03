---
layout: simple
title: "System Design: Skills Intelligence GraphRAG"
permalink: /system_design/design-skills-graphrag
---

# System Design: Skills Intelligence GraphRAG

## Combining Knowledge Graphs with Skills Ontology for Intelligent Talent Systems

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

```
Traditional Search:
  Query: "Python developer skills"
  Result: Documents mentioning "Python" ❌ No relationship context

GraphRAG:
  Query: "Python developer skills"
  Result:
    Python → [relates_to] → Data Analysis, Web Development, ML
    Python Developer → [requires] → Python, Git, SQL, APIs
    Python → [prerequisite_for] → TensorFlow, Django, FastAPI
  ✓ Rich, connected knowledge
```

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

### Python Implementation

```python
from neo4j import GraphDatabase
from openai import OpenAI
import json

class SkillsGraphRAG:
    """
    GraphRAG system for skills intelligence queries.
    """

    def __init__(self, neo4j_uri: str, neo4j_auth: tuple, openai_key: str):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=neo4j_auth)
        self.llm = OpenAI(api_key=openai_key)
        self.intent_classifier = IntentClassifier()

    def query(self, user_query: str) -> dict:
        """Process a natural language query about skills."""

        # Step 1: Classify intent and extract entities
        intent = self.intent_classifier.classify(user_query)
        entities = self._extract_entities(user_query)

        # Step 2: Generate and execute graph queries
        graph_context = self._get_graph_context(intent, entities)

        # Step 3: Get additional vector context (optional)
        vector_context = self._get_vector_context(user_query)

        # Step 4: Generate response with LLM
        response = self._generate_response(
            user_query, intent, graph_context, vector_context
        )

        return response

    def _extract_entities(self, query: str) -> dict:
        """Extract skills, professions, and other entities from query."""

        prompt = """
        Extract entities from this career/skills query:

        Query: {query}

        Return JSON with:
        - skills: list of skill names mentioned
        - professions: list of job titles/roles mentioned
        - certifications: list of certifications mentioned
        - industries: list of industries mentioned
        """

        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt.format(query=query)}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def _get_graph_context(self, intent: str, entities: dict) -> dict:
        """Query knowledge graph based on intent."""

        with self.driver.session() as session:
            if intent == "SKILLS_GAP":
                return self._skills_gap_query(session, entities)
            elif intent == "CAREER_PATH":
                return self._career_path_query(session, entities)
            elif intent == "SKILL_RECOMMENDATIONS":
                return self._skill_recommendations_query(session, entities)
            elif intent == "PROFESSION_SKILLS":
                return self._profession_skills_query(session, entities)
            else:
                return self._general_skills_query(session, entities)

    def _skills_gap_query(self, session, entities: dict) -> dict:
        """Find skills gap between current and target roles."""

        query = """
        // Get current role skills
        MATCH (current:Profession)
        WHERE current.name =~ $current_role
        OPTIONAL MATCH (current)-[:REQUIRES]->(cs:Skill)
        WITH current, collect(cs) as currentSkills

        // Get target role skills
        MATCH (target:Profession)
        WHERE target.name =~ $target_role
        OPTIONAL MATCH (target)-[r:REQUIRES]->(ts:Skill)
        WITH currentSkills, target, collect({skill: ts, importance: r.importance}) as targetSkills

        // Calculate gap
        WITH currentSkills, targetSkills,
             [t IN targetSkills WHERE NOT t.skill IN currentSkills] as gapSkills

        UNWIND gapSkills as gap
        OPTIONAL MATCH (gap.skill)-[:PREREQUISITE_FOR*0..2]-(related:Skill)
        OPTIONAL MATCH (gap.skill)-[:TAUGHT_BY]->(resource:LearningResource)

        RETURN gap.skill as skill,
               gap.importance as importance,
               collect(DISTINCT related) as related_skills,
               collect(DISTINCT resource) as learning_resources
        ORDER BY gap.importance DESC
        """

        result = session.run(query, {
            "current_role": f"(?i).*{entities['professions'][0]}.*",
            "target_role": f"(?i).*{entities['professions'][1]}.*"
        })

        return {"skills_gap": [dict(record) for record in result]}

    def _career_path_query(self, session, entities: dict) -> dict:
        """Find career progression paths."""

        query = """
        MATCH path = (start:Profession)-[:TRANSITIONS_TO*1..4]->(end:Profession)
        WHERE start.name =~ $start_role
        WITH path,
             [rel in relationships(path) | rel.difficulty] as difficulties,
             [node in nodes(path) | node.name] as roles
        RETURN roles,
               reduce(d = 0, x IN difficulties | d + x) as total_difficulty,
               length(path) as steps
        ORDER BY total_difficulty ASC
        LIMIT 5
        """

        result = session.run(query, {
            "start_role": f"(?i).*{entities['professions'][0]}.*"
        })

        return {"career_paths": [dict(record) for record in result]}

    def _skill_recommendations_query(self, session, entities: dict) -> dict:
        """Recommend skills based on current skills."""

        query = """
        // Match user's current skills
        UNWIND $skills as skillName
        MATCH (s:Skill)
        WHERE s.name =~ ('(?i).*' + skillName + '.*')
        WITH collect(s) as userSkills

        // Find related skills not in user's set
        UNWIND userSkills as us
        MATCH (us)-[:SIMILAR_TO|PREREQUISITE_FOR|RELATED_TO]-(recommended:Skill)
        WHERE NOT recommended IN userSkills

        // Score and rank recommendations
        WITH recommended,
             count(*) as relevance_score,
             avg(recommended.popularity) as popularity,
             avg(recommended.growth_rate) as growth

        RETURN recommended.name as skill,
               recommended.description as description,
               relevance_score,
               popularity,
               growth,
               (relevance_score * 0.4 + popularity * 0.3 + growth * 100 * 0.3) as total_score
        ORDER BY total_score DESC
        LIMIT 10
        """

        result = session.run(query, {"skills": entities.get('skills', [])})

        return {"recommendations": [dict(record) for record in result]}

    def _generate_response(self, query: str, intent: str,
                          graph_context: dict, vector_context: str) -> dict:
        """Generate final response using LLM."""

        prompt = f"""
        You are a career advisor with access to a skills knowledge graph.

        User Query: {query}
        Intent: {intent}

        Knowledge Graph Data:
        {json.dumps(graph_context, indent=2, default=str)}

        Additional Context:
        {vector_context}

        Provide a helpful, structured response that:
        1. Directly answers the user's question
        2. Cites specific skills and relationships from the graph
        3. Provides actionable recommendations
        4. Includes confidence level and caveats

        Format as JSON with:
        - summary: brief answer
        - details: detailed analysis
        - recommendations: list of actionable items
        - sources: graph paths used
        - confidence: 0-1 score
        """

        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


class IntentClassifier:
    """Classify user query intent."""

    INTENTS = [
        "SKILLS_GAP",           # What skills do I need for X?
        "CAREER_PATH",          # How do I become X?
        "SKILL_RECOMMENDATIONS", # What should I learn next?
        "PROFESSION_SKILLS",     # What skills does X need?
        "SKILL_COMPARISON",      # How do X and Y compare?
        "MARKET_TRENDS",         # What skills are in demand?
        "LEARNING_PATH",         # How do I learn X?
    ]

    def __init__(self):
        self.llm = OpenAI()

    def classify(self, query: str) -> str:
        prompt = f"""
        Classify this career/skills query into one of these intents:
        {self.INTENTS}

        Query: {query}

        Return only the intent name.
        """

        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()
```

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

```python
class SkillsEntityExtractor:
    """Extract skills entities from various sources."""

    def __init__(self):
        self.llm = OpenAI()
        self.textkernel_client = TextkernelClient()

    async def process_job_description(self, job_text: str) -> dict:
        """Extract skills and requirements from job description."""

        prompt = """
        Extract structured information from this job description:

        {text}

        Return JSON with:
        - job_title: string
        - required_skills: list of {{name, importance: "must"|"nice", level: "beginner"|"intermediate"|"expert"}}
        - responsibilities: list of strings
        - qualifications: list of strings
        - certifications: list of strings
        - experience_years: int or null
        - education: string or null
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt.format(text=job_text)}],
            response_format={"type": "json_object"}
        )

        extracted = json.loads(response.choices[0].message.content)

        # Enrich with Textkernel taxonomy IDs
        enriched_skills = []
        for skill in extracted['required_skills']:
            tk_match = await self.textkernel_client.match_skill(skill['name'])
            if tk_match:
                skill['textkernel_id'] = tk_match['id']
                skill['canonical_name'] = tk_match['canonical_name']
            enriched_skills.append(skill)

        extracted['required_skills'] = enriched_skills
        return extracted

    async def process_resume(self, resume_text: str) -> dict:
        """Extract skills and experience from resume."""

        prompt = """
        Extract structured information from this resume:

        {text}

        Return JSON with:
        - name: string
        - skills: list of {{name, proficiency: 1-5, years_experience: float}}
        - experience: list of {{title, company, duration_months, skills_used}}
        - education: list of {{degree, field, institution}}
        - certifications: list of {{name, provider, year}}
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt.format(text=resume_text)}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


class GraphBuilder:
    """Build and update the skills knowledge graph."""

    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
        self.entity_resolver = EntityResolver()

    def ingest_job(self, job_data: dict):
        """Add job and its skills to the graph."""

        with self.driver.session() as session:
            # Create or merge profession
            session.run("""
                MERGE (p:Profession {name: $title})
                SET p.updated_at = datetime()
            """, title=job_data['job_title'])

            # Add skills and relationships
            for skill in job_data['required_skills']:
                # Resolve skill to canonical form
                canonical = self.entity_resolver.resolve_skill(skill['name'])

                session.run("""
                    MERGE (s:Skill {id: $skill_id})
                    SET s.name = $name, s.updated_at = datetime()

                    WITH s
                    MATCH (p:Profession {name: $profession})
                    MERGE (p)-[r:REQUIRES]->(s)
                    SET r.importance = $importance,
                        r.level = $level,
                        r.count = coalesce(r.count, 0) + 1
                """,
                    skill_id=canonical['id'],
                    name=canonical['name'],
                    profession=job_data['job_title'],
                    importance=skill['importance'],
                    level=skill.get('level', 'intermediate')
                )

    def compute_skill_similarities(self):
        """Compute and store skill similarity relationships."""

        with self.driver.session() as session:
            # Find skills that co-occur in professions
            session.run("""
                MATCH (s1:Skill)<-[:REQUIRES]-(p:Profession)-[:REQUIRES]->(s2:Skill)
                WHERE id(s1) < id(s2)
                WITH s1, s2, count(p) as cooccurrence
                WHERE cooccurrence >= 3

                // Calculate Jaccard similarity
                MATCH (s1)<-[:REQUIRES]-(p1:Profession)
                WITH s1, s2, cooccurrence, count(DISTINCT p1) as s1_count
                MATCH (s2)<-[:REQUIRES]-(p2:Profession)
                WITH s1, s2, cooccurrence, s1_count, count(DISTINCT p2) as s2_count

                WITH s1, s2,
                     toFloat(cooccurrence) / (s1_count + s2_count - cooccurrence) as similarity
                WHERE similarity > 0.3

                MERGE (s1)-[r:SIMILAR_TO]-(s2)
                SET r.score = similarity, r.updated_at = datetime()
            """)
```

---

## 8. Implementation Details

### Complete System Setup

```python
# main.py - Skills GraphRAG System

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(title="Skills GraphRAG API")

# Initialize components
graph_rag = SkillsGraphRAG(
    neo4j_uri="bolt://localhost:7687",
    neo4j_auth=("neo4j", "password"),
    openai_key="sk-..."
)

# Request/Response Models
class QueryRequest(BaseModel):
    query: str
    context: Optional[dict] = None

class SkillsGapRequest(BaseModel):
    current_skills: List[str]
    target_profession: str

class CareerPathRequest(BaseModel):
    current_profession: str
    interests: Optional[List[str]] = None

# API Endpoints
@app.post("/query")
async def natural_language_query(request: QueryRequest):
    """Process natural language query about skills."""
    try:
        result = await graph_rag.query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/skills-gap")
async def analyze_skills_gap(request: SkillsGapRequest):
    """Analyze skills gap for a target profession."""
    try:
        result = await graph_rag.analyze_skills_gap(
            current_skills=request.current_skills,
            target_profession=request.target_profession
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/career-paths")
async def suggest_career_paths(request: CareerPathRequest):
    """Suggest career paths from current profession."""
    try:
        result = await graph_rag.suggest_career_paths(
            current_profession=request.current_profession,
            interests=request.interests
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/skill/{skill_name}")
async def get_skill_info(skill_name: str):
    """Get detailed information about a skill."""
    try:
        result = await graph_rag.get_skill_details(skill_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profession/{profession_name}/skills")
async def get_profession_skills(profession_name: str):
    """Get skills required for a profession."""
    try:
        result = await graph_rag.get_profession_skills(profession_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Docker Compose Setup

```yaml
# docker-compose.yml

version: '3.8'

services:
  neo4j:
    image: neo4j:5.15.0
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/password
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - neo4j

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  neo4j_data:
  neo4j_logs:
  redis_data:
```

---

## 9. Scalability & Performance

### Caching Strategy

```python
import redis
from functools import wraps
import hashlib
import json

class GraphRAGCache:
    """Multi-level caching for GraphRAG queries."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.local_cache = {}  # L1 cache
        self.ttl = {
            'graph_query': 3600,      # 1 hour
            'llm_response': 86400,    # 24 hours
            'entity_extraction': 604800  # 7 days
        }

    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from function arguments."""
        content = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        hash_val = hashlib.md5(content.encode()).hexdigest()
        return f"{prefix}:{hash_val}"

    def cached(self, prefix: str, ttl_key: str = 'graph_query'):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                key = self.cache_key(prefix, *args, **kwargs)

                # Check L1 cache
                if key in self.local_cache:
                    return self.local_cache[key]

                # Check Redis
                cached = self.redis.get(key)
                if cached:
                    result = json.loads(cached)
                    self.local_cache[key] = result
                    return result

                # Execute function
                result = await func(*args, **kwargs)

                # Store in caches
                self.redis.setex(key, self.ttl[ttl_key], json.dumps(result))
                self.local_cache[key] = result

                return result
            return wrapper
        return decorator


# Usage
cache = GraphRAGCache(redis.Redis())

class CachedSkillsGraphRAG(SkillsGraphRAG):

    @cache.cached('skills_gap')
    async def analyze_skills_gap(self, current_skills: list, target_profession: str):
        return await super().analyze_skills_gap(current_skills, target_profession)

    @cache.cached('career_path')
    async def suggest_career_paths(self, current_profession: str, interests: list):
        return await super().suggest_career_paths(current_profession, interests)
```

### Query Optimization

```cypher
// Create composite indexes for common query patterns
CREATE INDEX profession_skill_idx IF NOT EXISTS
FOR ()-[r:REQUIRES]-() ON (r.importance, r.weight);

// Precompute skill clusters for faster similarity queries
CALL gds.graph.project(
    'skills-graph',
    'Skill',
    {SIMILAR_TO: {properties: 'score'}}
)
YIELD graphName, nodeCount, relationshipCount;

CALL gds.louvain.write('skills-graph', {
    writeProperty: 'cluster'
})
YIELD communityCount, modularity;

// Use clusters for efficient recommendations
MATCH (target:Skill {name: $skill_name})
MATCH (similar:Skill)
WHERE similar.cluster = target.cluster
  AND similar <> target
RETURN similar
ORDER BY similar.popularity DESC
LIMIT 10;
```

---

## 10. Advanced Features

### 10.1 Trend Analysis

```python
class SkillsTrendAnalyzer:
    """Analyze skill trends over time."""

    def __init__(self, driver):
        self.driver = driver

    def compute_growth_rates(self):
        """Compute skill demand growth rates."""

        with self.driver.session() as session:
            session.run("""
                MATCH (s:Skill)<-[r:REQUIRES]-(p:Profession)
                WHERE r.created_at IS NOT NULL

                WITH s,
                     count(CASE WHEN r.created_at > datetime() - duration('P30D')
                           THEN 1 END) as recent_mentions,
                     count(CASE WHEN r.created_at > datetime() - duration('P90D')
                           AND r.created_at <= datetime() - duration('P30D')
                           THEN 1 END) as older_mentions

                WHERE older_mentions > 0
                SET s.growth_rate = toFloat(recent_mentions - older_mentions) / older_mentions,
                    s.trend = CASE
                        WHEN recent_mentions > older_mentions * 1.2 THEN 'rising'
                        WHEN recent_mentions < older_mentions * 0.8 THEN 'declining'
                        ELSE 'stable'
                    END
            """)

    def get_trending_skills(self, industry: str = None, limit: int = 20) -> list:
        """Get currently trending skills."""

        with self.driver.session() as session:
            query = """
                MATCH (s:Skill)
                WHERE s.growth_rate > 0.1
            """

            if industry:
                query += """
                    AND EXISTS {
                        MATCH (s)<-[:REQUIRES]-(p:Profession)-[:BELONGS_TO]->(i:Industry)
                        WHERE i.name = $industry
                    }
                """

            query += """
                RETURN s.name as skill,
                       s.growth_rate as growth,
                       s.trend as trend
                ORDER BY s.growth_rate DESC
                LIMIT $limit
            """

            result = session.run(query, industry=industry, limit=limit)
            return [dict(r) for r in result]
```

### 10.2 Personalized Recommendations

```python
class PersonalizedRecommender:
    """Generate personalized skill recommendations."""

    def __init__(self, graph_rag: SkillsGraphRAG):
        self.graph_rag = graph_rag

    async def recommend_for_user(self, user_profile: dict) -> dict:
        """Generate personalized recommendations based on user profile."""

        # Build user context
        context = {
            'current_skills': user_profile.get('skills', []),
            'experience_years': user_profile.get('experience', 0),
            'goals': user_profile.get('career_goals', []),
            'interests': user_profile.get('interests', []),
            'learning_style': user_profile.get('learning_style', 'self-paced')
        }

        # Get skill recommendations
        skill_recs = await self._get_skill_recommendations(context)

        # Get career path recommendations
        career_recs = await self._get_career_recommendations(context)

        # Get learning resource recommendations
        learning_recs = await self._get_learning_recommendations(
            skill_recs, context['learning_style']
        )

        return {
            'skills_to_learn': skill_recs,
            'career_paths': career_recs,
            'learning_resources': learning_recs,
            'personalization_factors': self._explain_recommendations(context)
        }

    async def _get_skill_recommendations(self, context: dict) -> list:
        """Get personalized skill recommendations."""

        query = """
        // Match user's current skills
        UNWIND $skills as skillName
        MATCH (current:Skill)
        WHERE current.name =~ ('(?i).*' + skillName + '.*')
        WITH collect(current) as currentSkills

        // Find skills that lead to user's goal professions
        UNWIND $goals as goalName
        MATCH (goal:Profession)
        WHERE goal.name =~ ('(?i).*' + goalName + '.*')
        MATCH (goal)-[:REQUIRES]->(needed:Skill)
        WHERE NOT needed IN currentSkills

        // Score by relevance to goals and market demand
        WITH needed,
             count(DISTINCT goal) as goal_relevance,
             needed.growth_rate as growth,
             needed.popularity as popularity

        RETURN needed.name as skill,
               needed.description as description,
               goal_relevance,
               growth,
               popularity,
               (goal_relevance * 0.4 + growth * 0.3 + popularity/100 * 0.3) as score
        ORDER BY score DESC
        LIMIT 10
        """

        with self.graph_rag.driver.session() as session:
            result = session.run(query,
                skills=context['current_skills'],
                goals=context['goals']
            )
            return [dict(r) for r in result]
```

### 10.3 Natural Language to Cypher

```python
class NL2Cypher:
    """Convert natural language to Cypher queries."""

    SCHEMA_DESCRIPTION = """
    Graph Schema:
    - Nodes: Skill (name, type, description, popularity, growth_rate)
    - Nodes: Profession (name, industry, seniority, avg_salary)
    - Nodes: Category (name, parent_id)
    - Nodes: Certification (name, provider, validity)
    - Nodes: LearningResource (title, type, duration, provider)

    - Relationships:
      - (Profession)-[:REQUIRES {importance, weight}]->(Skill)
      - (Skill)-[:SIMILAR_TO {score}]->(Skill)
      - (Skill)-[:PREREQUISITE_FOR]->(Skill)
      - (Skill)-[:BELONGS_TO]->(Category)
      - (Skill)-[:VALIDATED_BY]->(Certification)
      - (Skill)-[:TAUGHT_BY]->(LearningResource)
      - (Profession)-[:TRANSITIONS_TO {difficulty}]->(Profession)
    """

    def __init__(self):
        self.llm = OpenAI()

    async def generate_cypher(self, natural_query: str) -> str:
        """Generate Cypher query from natural language."""

        prompt = f"""
        Convert this natural language query to a Cypher query.

        {self.SCHEMA_DESCRIPTION}

        Natural Language Query: {natural_query}

        Guidelines:
        - Use case-insensitive regex for name matching: name =~ '(?i).*term.*'
        - Always return relevant properties
        - Use OPTIONAL MATCH for optional relationships
        - Limit results to avoid overwhelming output

        Return only the Cypher query, no explanation.
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()
```

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

## References

- [Textkernel Skills Intelligence API](https://developer.textkernel.com/SkillsIntelligence/master/ontology/)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/)
- [LangChain Graph QA](https://python.langchain.com/docs/use_cases/graph/)
