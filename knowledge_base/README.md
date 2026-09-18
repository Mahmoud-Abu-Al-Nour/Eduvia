# Eduvia Knowledge Base

This directory contains educational knowledge documents used by the RAG system.

## Purpose

The knowledge base provides Gemini with grounded educational context for:
- Activity generation
- Strategy recommendations
- Scaffolding approaches
- Accessibility guidelines

## Structure

```
knowledge_base/
├── README.md
└── sources/
    ├── strategies/          Teaching strategy documents
    ├── curriculum/          Curriculum design principles
    ├── accessibility/       Accessibility guidelines
    └── activity_design/     Activity design principles
```

## How It Works (Phase 9)

1. Documents are chunked into ~500 token segments
2. Chunks are embedded using a text embedding model
3. Embeddings are stored in Qdrant `eduvia_knowledge` collection
4. At generation time, relevant chunks are retrieved via semantic search
5. Retrieved chunks are included in the Gemini prompt as context

## Adding Knowledge

Place markdown or plain text files in the appropriate `sources/` subdirectory.
Run the ingestion script (Phase 9) to embed and index them.

## Important Notes

- This is NOT a medical or psychological knowledge base
- Content must use educational (not diagnostic) language
- Knowledge is used to GUIDE generation, not generate autonomously
