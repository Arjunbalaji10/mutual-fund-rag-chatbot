# Product Requirements Document (PRD)

## 1. Product Goal

Build a small RAG-based Mutual Fund FAQ chatbot that answers factual questions about selected HDFC mutual fund schemes using only the information available in the approved public source documents.

The chatbot must provide a source link with every answer and must not provide investment advice.

## 2. Target Users

### Primary Users
Retail mutual fund users who want quick factual information about mutual fund schemes.

### Secondary Users
Support and content teams who answer repetitive mutual fund questions.

## 3. In Scope

The chatbot will:

- Support one AMC: HDFC.
- Support 3–5 HDFC mutual fund schemes.
- Answer factual questions about:
  - Expense ratio
  - Exit load
  - Minimum SIP
  - ELSS lock-in period
  - Riskometer
  - Benchmark
  - Statement and tax-document download information
- Retrieve information from the approved source data using RAG.
- Provide one source link with every answer.
- Keep answers to 3 sentences or fewer.
- Show when the information was last updated from the sources.
- Refuse investment advice and portfolio-related questions.
- Say that the information is unavailable when the retrieved sources do not contain the answer.

## 4. Out of Scope

The chatbot will not:

- Recommend a mutual fund to a user.
- Tell a user whether to buy or sell a fund.
- Provide personalized investment advice.
- Calculate or compare investment returns.
- Accept or store PAN, Aadhaar, bank account numbers, OTPs, phone numbers, or email addresses.
- Use third-party blogs as information sources.
- Use private or backend application data.

## 5. Example User Questions

The chatbot should be able to handle questions such as:

1. What is the expense ratio of HDFC Large Cap Fund?
2. What is the exit load?
3. What is the minimum SIP amount?
4. What is the lock-in period for HDFC ELSS Tax Saver Fund?
5. What is the riskometer of this scheme?
6. What is the benchmark of the fund?
7. How can I download my capital-gains statement?
8. Should I buy this mutual fund?

The last question should be refused because it asks for investment advice.

## 6. Success Criteria

The product is successful when:

- The chatbot retrieves relevant information from the source data.
- Answers are based only on the retrieved source information.
- Every factual answer contains a clear source link.
- The chatbot refuses investment advice.
- The chatbot does not invent information when the source data does not contain an answer.
- The RAG pipeline successfully retrieves relevant chunks for user questions.
- The vector database persists between application restarts.
- The chatbot can be run locally and deployed to Render.

## 7. Technical Constraints

### Embedding Model

Use:

sentence-transformers/all-MiniLM-L6-v2

The same embedding model must be used for source chunks and user questions.

### Vector Database

Use ChromaDB with persistent storage.

### LLM

Use Groq.

The Groq API key must be stored in `.env` and must never be committed to GitHub.

### RAG Pipeline

Data ingestion:

Load → Chunk → Embed → Store in Vector DB

Data retrieval:

Question → Embed → Retrieve relevant chunks → LLM → Answer

## 8. Source Constraints

Use only approved public sources.

Sources may include:

- AMC
- SEBI
- AMFI

Do not use third-party blogs as sources.

## 9. User Interface

The UI should contain:

- A welcome message.
- Three example questions.
- A clear note:

"Facts-only. No investment advice."

- Chat message history.
- Source information for each answer.
- A clear-chat option.