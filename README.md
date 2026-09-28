# RAG-based Mutual Fund FAQ Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers factual questions about selected HDFC Mutual Fund schemes using information collected from public source pages.

The chatbot is designed to provide factual information only. It does not provide investment advice, recommendations, or predictions about future returns.

---

## 1. Problem Statement

Mutual fund information is spread across different pages and can be difficult to find quickly.

This project builds a factual Mutual Fund FAQ assistant that allows users to ask questions about selected HDFC Mutual Fund schemes and receive concise answers with a source link.

---

## 2. Product Goal

Build a simple and reliable Mutual Fund FAQ assistant that:

- Answers factual mutual fund questions.
- Uses a Retrieval-Augmented Generation (RAG) pipeline.
- Provides a source link with the answer.
- Refuses investment advice and recommendations.
- Refuses unrelated questions.
- Keeps answers concise.

---

## 3. Target Users

The chatbot is designed for users who want to quickly find factual information about mutual fund schemes, such as:

- Expense ratio
- Exit load
- Minimum SIP amount
- Risk level
- Benchmark
- ELSS lock-in period
- Tax and statement-related information

---

## 4. Mutual Fund Schemes Covered

The current knowledge base contains five HDFC Mutual Fund schemes:

1. HDFC Large Cap Fund Direct Growth
2. HDFC Equity Fund Direct Growth
3. HDFC ELSS Tax Saver Fund Direct Plan Growth
4. HDFC Small Cap Fund Direct Growth
5. HDFC Balanced Advantage Fund Direct Growth

---

## 5. Key Features

### Factual FAQ Answers

Users can ask factual questions about the supported mutual fund schemes.

### RAG-based Retrieval

The system retrieves relevant information from the knowledge base before generating an answer.

### Source Links

Each answer provides the source page used for the relevant scheme.

### Guardrails

The chatbot:

- Does not provide investment recommendations.
- Does not answer questions about buying or selling funds.
- Does not make future performance claims.
- Rejects unrelated questions.

### Conversation History

The Streamlit interface maintains the conversation during the session.

### Clear Chat

Users can clear the current conversation using the Clear Chat button.

---

## 6. RAG Architecture

The system follows this flow:

```text
Public Source Pages
        ↓
Data Collection
        ↓
Raw Text
        ↓
Chunking
        ↓
Text Embeddings
        ↓
ChromaDB
        ↓
User Question
        ↓
Question Embedding
        ↓
Relevant Chunk Retrieval
        ↓
Groq LLM
        ↓
Factual Answer + Source