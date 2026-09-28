# Implementation Plan

## Overview

The RAG chatbot will be implemented in six phases.

Each phase must be completed and verified before moving to the next phase.

---

# Phase 1 — Project Setup

## Goal

Set up the Python project structure, dependencies, environment configuration, and Git security rules.

## Files to create

- requirements.txt
- .gitignore
- .env.example
- src/
- data/
- docs/

## What this phase does

- Creates the project folder structure.
- Defines Python dependencies.
- Creates a .gitignore file.
- Ensures .env, virtual environments, and __pycache__ are not committed.
- Creates the initial source-code structure.

## Verification

Verify that:

1. The project structure exists.
2. requirements.txt exists.
3. .gitignore excludes .env, venv, and __pycache__.
4. The project can install its dependencies successfully.

---

# Phase 2 — Loading and Chunking

## Goal

Load the approved source data and divide it into inspectable chunks.

## Files to create

- Source ingestion/loading files under src/
- data/raw/
- data/chunks/chunks.txt

## What this phase does

1. Loads the approved source documents.
2. Stores raw source text under data/raw/.
3. Splits the source content into chunks.
4. Stores every chunk in data/chunks/chunks.txt.
5. Includes chunk numbering, source information, and character count.

## Chunking strategy

Before implementing chunking, inspect the source data and determine an appropriate:

- Chunk size
- Chunk overlap
- Metadata structure

The reasoning for the chunking strategy should be documented.

## Verification

Verify that:

1. Raw source data exists under data/raw/.
2. chunks.txt exists.
3. Chunks are numbered.
4. Each chunk contains source information.
5. Character counts are available.
6. The number of chunks created is known.
7. The chunks can be manually inspected.

---

# Phase 3 — Embedding and Vector Store

## Goal

Convert the chunks into embeddings and store them in persistent ChromaDB.

## Files to create

- Embedding/vector-store implementation under src/
- Persistent ChromaDB directory
- data/embeddings_preview.txt

## What this phase does

1. Loads the chunks.
2. Uses sentence-transformers/all-MiniLM-L6-v2 to create embeddings.
3. Stores the embeddings and metadata in ChromaDB.
4. Uses a persistent ChromaDB directory.
5. Creates a preview of the first five embeddings.

## Verification

Verify that:

1. The embedding model works.
2. Embeddings are created for the chunks.
3. ChromaDB contains the expected number of vectors.
4. data/embeddings_preview.txt exists.
5. The preview contains the first five embeddings.
6. The first ten dimensions of the previewed embeddings can be inspected.
7. The ChromaDB data persists after restarting the application.

---

# Phase 4 — Guardrails

## Goal

Prevent the chatbot from answering questions outside the intended facts-only scope.

## What this phase does

The system should:

- Refuse off-topic questions.
- Refuse investment advice.
- Refuse portfolio recommendations.
- Avoid making claims that are not supported by source content.
- Say "I don't know" when the retrieved context does not answer the question.
- Avoid handling or storing prohibited personal information.

## Verification

Test questions should include:

1. An answerable mutual fund factual question.
2. An off-topic question.
3. An investment-advice question.
4. A question for which the source data does not contain an answer.
5. A question containing prohibited personal information.

Verify that the chatbot responds according to the guardrail requirements.

---

# Phase 5 — Retrieval and LLM Answer

## Goal

Build the complete RAG retrieval and answer-generation pipeline.

## Files to create

- Retrieval implementation under src/
- LLM integration under src/
- CLI testing script

## What this phase does

1. Accepts a user question.
2. Embeds the question using the same embedding model used during Phase 3.
3. Searches ChromaDB.
4. Retrieves the top-k relevant chunks.
5. Builds the LLM context using:
   - System prompt
   - Retrieved chunks
   - User question
6. Sends the context to the Groq LLM.
7. Generates a facts-only answer.
8. Shows the retrieved chunks during testing.

## Conversation memory

Add conversation memory that keeps the last 10 messages.

Use the conversation history to rewrite follow-up questions before retrieval.

Example:

User:
"What is the expense ratio of HDFC Large Cap Fund?"

Follow-up:
"What about its fees?"

The system should resolve "its" using the previous conversation context before performing retrieval.

## Verification

Test:

- Direct factual questions.
- Follow-up questions.
- Questions requiring retrieval.
- Questions with no supporting context.
- Off-topic questions.
- Investment-advice questions.

Verify which chunks were retrieved for each test question.

---

# Phase 6 — User Interface

## Goal

Build a simple chat interface for the completed RAG pipeline.

## Technology

Streamlit.

## UI requirements

The UI should contain:

- Welcome message.
- Three example questions.
- Chat message history.
- Source information under each answer.
- Clear-chat button.
- Facts-only / no-investment-advice notice.

## Verification

Verify that:

1. The application starts locally.
2. A user can submit a question.
3. The RAG pipeline retrieves relevant context.
4. The answer is displayed.
5. The source is displayed.
6. Conversation history works.
7. Clear-chat works.
8. Guardrails work through the UI.

---

# Final Testing

Before deployment, test:

1. Factual questions with answers in the source data.
2. Questions with no answer in the source data.
3. Off-topic questions.
4. Investment-advice questions.
5. Follow-up questions using conversation memory.
6. Source links.
7. Last-updated information.
8. Privacy restrictions.
9. ChromaDB persistence.
10. UI functionality.

---

# Deployment

After the six phases are verified:

1. Create a GitHub repository.
2. Ensure .env is not committed.
3. Ensure the ChromaDB directory is not committed.
4. Push the project to GitHub.
5. Deploy the application to Render.
6. Rebuild the vector database during the Render build.
7. Configure the required environment variables.
8. Test the deployed application.