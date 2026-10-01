# Local Research Paper RAG Project

A fully local Retrieval-Augmented Generation (RAG) application that uses embedding-based semantic search to retrieve relevant research paper abstracts and provide them as context to a local language model for grounded question answering.

The project uses Microsoft's Foundry Local SDK to run both the embedding model and chat model locally, without requiring requiring a cloud-based inference API.

## Overview

This project implements a basic RAG pipeline for searching and asking questions about a collection of research papers.

Given a user question, the application:

1. Generates an embedding for the user's question.
2. Compares the query embedding against embeddings of research paper abstracts.
3. Retrieves the 5 most semantically similar papers using cosine similarity.
4. Provides the retrieved abstracts as context to a local language model.
5. Generates a response based on the retrieved context.

## Architecture

```
                    Research Papers
                          │
                          ▼
                 ┌─────────────────┐
                 │ Embedding Model │
                 │ qwen3-embedding │
                 │     -0.6b       │
                 └────────┬────────┘
                          │
                          ▼
                Abstract Embeddings
                          │
                          │
User Question ────────────┤
       │                  │
       ▼                  ▼
┌──────────────┐   ┌─────────────────┐
│ Query        │   │ Cosine          │
│ Embedding    │──►│ Similarity      │
└──────────────┘   └────────┬────────┘
                            │
                            ▼
                      Top 5 Papers
                            │
                            ▼
                  ┌──────────────────┐
                  │ Retrieved        │
                  │ Context          │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Local Chat Model │
                  │ qwen2.5-0.5b     │
                  └────────┬─────────┘
                           │
                           ▼
                         Answer
```

## Key Features

- Fully local embedding and text generation
- Semantic search using vector embeddings
- Cosine similarity-based document retrieval
- Top-5 relevant paper retrieval
- Batched embedding generation
- Streaming model responses
- Context-grounded question answering
- Basic hallucination prevention instructions

## Tech Stack

- Python
- Microsoft Foundry Local SDK
- Qwen3 Embedding 0.6B — document and query embeddings
- Qwen2.5 0.5B — answer generation
- Cosine similarity
- JSON

## Examples

Example questions and model responses can be found in [examples.md](examples.md).

The examples demonstrate three types of interactions with the RAG system:
- **General questions** about topics covered by the research papers
- **Follow-up questions** based on a previous question
- **Paper-specific questions** asking for particular papers

## Future Improvements

- Persist document embeddings between runs
- Introduce a vector database for scalable retrieval
- Add retrieval and response evaluation metrics
- Improve response grounding to reduce unsupported claims