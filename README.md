# RAG-based Mutual Fund FAQ Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers factual questions about selected HDFC Mutual Fund schemes.

The chatbot provides factual information only. It does not provide investment advice or recommendations.

## Problem Statement

Mutual fund information is available across different pages and can be difficult to find quickly.

This project provides a simple chatbot where users can ask factual questions about selected HDFC Mutual Fund schemes and receive concise answers with a source link.

## Product Goal

The chatbot aims to:

- Answer factual mutual fund questions.
- Use a RAG pipeline.
- Provide source links.
- Reject investment advice requests.
- Reject unrelated questions.
- Reject unsupported funds.
- Keep answers concise.

## Supported Mutual Funds

The knowledge base currently covers:

1. HDFC Large Cap Fund Direct Growth
2. HDFC Equity Fund Direct Growth
3. HDFC ELSS Tax Saver Fund Direct Plan Growth
4. HDFC Small Cap Fund Direct Growth
5. HDFC Balanced Advantage Fund Direct Growth

## Key Features

- Factual FAQ answers
- RAG-based retrieval
- Source links
- Investment advice guardrails
- Off-topic question guardrails
- Unsupported fund guardrails
- Conversation history
- Clear Chat button

## RAG Architecture

The system works as follows:

Source Pages
↓
Data Collection
↓
Text Chunking
↓
Embeddings
↓
ChromaDB
↓
User Question
↓
Relevant Chunk Retrieval
↓
Groq LLM
↓
Answer + Source

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- Groq API
- BeautifulSoup
- Requests
- python-dotenv

Embedding model:

all-MiniLM-L6-v2

Vector database:

ChromaDB

LLM:

openai/gpt-oss-20b using Groq API

## Project Structure

mutual-fund-rag-chatbot/

data/
raw/

docs/

src/
app.py
collect_sources.py
chunk_sources.py
embed_store.py
guardrails.py
rag_pipeline.py

.env.example
.gitignore
ProblemStatement.txt
README.md
requirements.txt

## Setup

### 1. Create a virtual environment

```text
python -m venv .venv