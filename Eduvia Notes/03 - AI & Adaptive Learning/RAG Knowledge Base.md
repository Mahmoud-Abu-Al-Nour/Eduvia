# RAG Knowledge Base

The Retrieval-Augmented Generation (RAG) system grounds LLM generation in verified pedagogical literature.

---

## Qdrant Collections

1. **`eduvia_knowledge`**:
   - Evidence-based special education literature.
   - Universal Design for Learning (UDL) guidelines.
   - Neurodiversity and cognitive processing accommodations.
   - Verified scaffolding strategies.

2. **`eduvia_curriculum`**:
   - Embeddings of standardized curriculum objectives and lesson definitions.
   - Facilitates semantic cross-referencing and prerequisite alignment.

---

## Retrieval Protocol
During activity generation, the Orchestrator queries Qdrant using embeddings of the objective and target strategy, injecting the top matching pedagogical passages into the LLM system context. This prevents generic or hallucinated teaching methods.
