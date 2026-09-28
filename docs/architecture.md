# RAG Chatbot Architecture

## 1. System Overview

The system is a Retrieval-Augmented Generation (RAG) chatbot for answering factual questions about selected HDFC mutual fund schemes.

The chatbot uses approved public source data as its knowledge base.

It does not provide investment advice.

## 2. Architecture Components

The system contains these major components:

1. Source Documents
2. Data Loader
3. Chunking Component
4. Embedding Model
5. ChromaDB Vector Database
6. Query and Retrieval Component
7. Groq LLM
8. Guardrails
9. Chat UI

## 3. Data Ingestion Flow

Source Documents
        ↓
      Load
        ↓
     Chunk
        ↓
     Embed
        ↓
   ChromaDB

### Load

Read the approved public source documents and convert them into text that can be processed.

### Chunk

Split the source text into smaller chunks that can be retrieved when a user asks a question.

The chunking strategy will be decided after inspecting the source data.

Each chunk should retain useful metadata such as its source.

### Embed

Use:

sentence-transformers/all-MiniLM-L6-v2

The same embedding model will be used for source chunks and user questions.

The model produces 384-dimensional vectors.

### Store

Store the embeddings and their associated text and metadata in persistent ChromaDB.

The vector database should persist to disk so that ingestion does not need to run every time the application starts.

## 4. Query and Retrieval Flow

User Question
      ↓
Question Embedding
      ↓
Search ChromaDB
      ↓
Retrieve Top-K Relevant Chunks
      ↓
Guardrails / Context Check
      ↓
Groq LLM
      ↓
Final Answer + Source

### Question Embedding

The user's question is converted into an embedding using the same:

sentence-transformers/all-MiniLM-L6-v2

model used during ingestion.

### Retrieval

The question embedding is compared with the stored vectors in ChromaDB.

The most relevant chunks are retrieved.

### Context Augmentation

The retrieved chunks are provided to the LLM together with:

- System instructions
- User question
- Retrieved source context

### Answer Generation

Groq generates the final answer using the retrieved context.

The chatbot should not invent information that is not supported by the retrieved source content.

## 5. Guardrails

The chatbot must:

- Answer factual mutual fund questions only.
- Refuse investment advice and portfolio recommendations.
- Not provide buy or sell recommendations.
- Not provide personalized investment advice.
- Say that the information is unavailable when the source context does not answer the question.
- Not accept or store PII such as PAN, Aadhaar, account numbers, OTPs, emails, or phone numbers.
- Provide a source link with factual answers.

## 6. Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| LLM | Groq |
| UI | Streamlit |
| Environment Variables | .env |
| Deployment | Render |

## 7. High-Level Query Diagram

User
  |
  v
Chat UI
  |
  v
Question
  |
  v
Embedding Model
  |
  v
ChromaDB
  |
  v
Top-K Relevant Chunks
  |
  v
Guardrails
  |
  v
Groq LLM
  |
  v
Answer + Source Link

## 8. Project Structure

The planned project structure is:

milestone-4-rag-chatbot/
│
├── data/
│   ├── raw/
│   ├── chunks/
│   └── embeddings_preview.txt
│
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   └── implementation.md
│
├── src/
│   ├── ingest/
│   └── ...
│
├── ProblemStatement.txt
├── requirements.txt
├── .env
├── .env.example
└── .gitignore

The exact source-code files will be finalized in the implementation plan.

## 9. Environment and Security

The Groq API key must be stored in `.env`.

The `.env` file must not be committed to GitHub.

A `.env.example` file will document the required environment variables without containing the real API key.