# Eduvia AI & RAG Technical Approach

> **Bounded Generative AI, Retrieval-Augmented Grounding, and Absolute Deterministic Safeguards**

---

## Architectural Role of AI in Eduvia

In many EdTech applications, generative AI is deployed as an open-ended conversational chatbot or an unconstrained decision-making agent. This architecture is unacceptable in special education:
* Open-ended chatbots hallucinate facts and can provide confusing or pedagogically inappropriate explanations.
* Black-box AI decision engines cannot provide deterministic guarantees, making compliance with Individualized Education Programs (IEPs) impossible.
* API rate limits, network outages, or model latency can leave a vulnerable learner stranded mid-lesson.

Eduvia takes a fundamentally different engineering approach: **Generative AI is bounded, schema-constrained, grounded in verified pedagogical literature via RAG, and backed by a 100% deterministic fallback generator.**

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                Pedagogical Knowledge Base                   │
 │   Universal Design for Learning (UDL) • Scaffolding Guides  │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Semantic Chunking & UUIDv5
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                 Qdrant Vector Database                      │
 │    `eduvia_knowledge` & `eduvia_curriculum` (768 dims)      │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Filtered Semantic Retrieval
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │             Grounded Prompt Synthesis Engine                │
 │   Objective + Learner Accommodations + Retrieved Evidence   │
 └──────────────────────────────┬──────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼ (Online / API Active)                         ▼ (Offline / Failover)
┌───────────────────────────────┐       ┌───────────────────────────────┐
│     Gemini 2.5 Flash API      │       │ Deterministic Fallback Engine │
│  Modern `google-genai` SDK    │       │     Zero-Strand Guarantee     │
│  Schema-Constrained JSON Gen  │       │ Pre-Validated Structured DTOs │
└───────────────┬───────────────┘       └───────────────┬───────────────┘
                │                                       │
                └───────────────────┬───────────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │ Pydantic v2 Schema Validator│
                     │  Strict Discriminated Union │
                     └──────────────┬──────────────┘
                                    ▼
                      Valid Activity Ready for Client
```

---

## 1. Generative AI Engine: Gemini 2.5 Flash

### SDK Migration & Modern Architecture
Eduvia utilizes the official, modern **Google GenAI SDK** (`from google import genai`) targeting **Gemini 2.5 Flash**. The legacy deprecated `google.generativeai` package has been completely eliminated from the codebase, ensuring zero deprecation warnings and future-proof compatibility.

### Schema-Constrained Generation
The platform never solicits raw, unstructured markdown from the LLM. Every generation request utilizes structured output constraints:
* Prompts specify strict JSON schemas corresponding to the target modality (`matching`, `multiple_choice`, `ordering`, `visual_identification`, or `drag_and_drop`).
* Responses are parsed and validated immediately against Pydantic models.
* If the model produces malformed JSON or omits required fields (e.g., missing distractors or missing target keys), the system detects the anomaly and triggers fallback generation.

---

## 2. Why Deterministic Fallbacks Exist: The Zero-Strand Guarantee

In an educational setting with neurodivergent students, an error screen ("API Connection Failed", "500 Internal Error", or an infinite loading spinner) can trigger severe frustration and disengagement.

Eduvia enforces the **Zero-Strand Guarantee**:
* The system contains a fully offline, deterministic activity generator (`activities/fallback.py`).
* If Gemini is unavailable, if API keys are missing, if quota limits are exceeded, or if network connectivity is severed, the system instantly synthesizes a pedagogically valid, curriculum-aligned activity from its deterministic template library.
* The learner experience is never interrupted. The frontend receives a fully compliant `ActivityData` object within milliseconds, with metadata flagging `generated_by: "fallback"`.

---

## 3. Knowledge Ingestion & Vector Indexing Pipeline

To ground generative output in empirical educational practices, Eduvia maintains a specialized Retrieval-Augmented Generation (RAG) vector repository backed by **Qdrant**.

### Ingestion Flow
```text
Markdown Pedagogical Docs (UDL, Accommodations, Scaffolding)
                          │
                          ▼
             Semantic Boundary Chunking
       (Passages split by logical subheadings)
                          │
                          ▼
           Deterministic UUIDv5 Generation
    (Hash of document namespace + chunk content)
                          │
                          ▼
     Dense Embedding: `text-embedding-004`
           (768-dimensional float vectors)
                          │
                          ▼
             Qdrant Upsert (Idempotent)
    (`eduvia_knowledge` & `eduvia_curriculum`)
```

### Deterministic Identifiers & Deduplication
To ensure idempotence and prevent database bloat during repeated deployments:
* Every knowledge chunk is hashed using **UUIDv5** with a project-specific DNS namespace.
* Re-running the ingestion pipeline (`python -m app.services.knowledge.ingestion`) updates existing vectors in place without creating duplicate points.

---

## 4. Semantic Retrieval & Grounded Generation

When generating an activity for a specific learning objective, the system executes a grounded retrieval workflow:

1. **Query Construction**: The search query is synthesized from the objective title, grade level, target modality, and the learner's recorded sensory profile.
2. **Filtered Vector Search**: Qdrant executes cosine similarity search over `eduvia_knowledge`, applying metadata filters (e.g., filtering for visual accommodations if the learner has high visual affinity).
3. **Prompt Grounding**: The top-$k$ retrieved pedagogical evidence passages are injected into the Gemini system prompt:
   ```text
   You are an expert curriculum designer. Generate an accessible activity following 
   these verified pedagogical strategies:
   [GROUNDING CONTEXT: Universal Design for Learning Guideline 2.5...]
   [GROUNDING CONTEXT: Scaffolding for working memory deficit...]
   ```
4. **Source Attribution**: The IDs and document titles of the retrieved chunks are attached to the activity metadata as `grounding_sources`. Teachers can inspect the exact evidence base used to shape their student's activity.

---

## 5. Non-Negotiable AI Safety Boundaries

Eduvia maintains strict architectural firewalls regarding AI capabilities:

| AI Boundary | Enforcement Mechanism |
| :--- | :--- |
| **No Autonomous Tutors / Chatbots** | Eduvia provides structured activity interactions (options, ordering, dragging). Free-form open text generation toward learners is strictly disabled to prevent hallucinations or inappropriate dialogue. |
| **No Clinical or Medical Diagnosis** | The system assesses academic objective mastery and sensory modality affinity. It explicitly refrains from diagnosing autism, ADHD, dyslexia, or any cognitive pathology. |
| **No Decision Authority Over Adaptation** | The AI never evaluates whether a student has passed, never assigns mastery levels, and never routes a student to a new curriculum node. All progression logic is deterministic Python code. |
| **No Unbounded Generation** | Every LLM response is bounded by Pydantic models. Malformed or out-of-bounds responses are discarded. |
| **Full Teacher Visibility** | All generated activities and grounding sources are logged and inspectable by educators. |

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Personalization & Adaptation: [[Eduvia Learning & Personalization Approach|Eduvia Learning & Personalization Approach]]
* RAG Knowledge Base Details: [[03 - AI & Adaptive Learning/RAG Knowledge Base|RAG Knowledge Base]]
* Gemini Integration Architecture: [[03 - AI & Adaptive Learning/Gemini Integration|Gemini Integration]]
* AI Decision Governance: [[06 - Decisions/AI Decisions|AI Decisions]]
* Phase 9 Implementation History: [[05 - Development History/Phase 09 — Gemini Production & RAG Ingestion|Phase 09 — Gemini Production & RAG Ingestion]]
