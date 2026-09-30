# RAG-based Mutual Fund FAQ Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers factual questions about selected HDFC Mutual Fund schemes.

The chatbot provides factual information only. It does not provide investment advice or recommendations.

## Problem Statement

Mutual fund information is available across different pages and can be difficult to find quickly.

This project provides a simple chatbot where users can ask factual questions about selected HDFC Mutual Fund schemes and receive concise answers with a source link.

## Product Goal

The chatbot aims to:

- Answer factual mutual fund questions.
- Retrieve relevant information from the knowledge base.
- Provide source links.
- Reject investment advice requests.
- Reject unrelated questions.
- Reject unsupported funds.
- Keep answers concise.

## Supported Mutual Funds

The current knowledge base covers:

1. HDFC Large Cap Fund Direct Growth
2. HDFC Equity Fund Direct Growth
3. HDFC ELSS Tax Saver Fund Direct Plan Growth
4. HDFC Small Cap Fund Direct Growth
5. HDFC Balanced Advantage Fund Direct Growth

## Key Features

- Factual FAQ answers
- Retrieval-based question answering
- Source links
- Investment advice guardrails
- Off-topic question guardrails
- Unsupported fund guardrails
- Conversation history
- Clear Chat button
- Three example questions in the UI
- Facts-only disclaimer

## RAG Architecture

### Data Ingestion Flow

```text
Source Pages
    ↓
Data Collection
    ↓
Text Chunking
    ↓
Embedding
    ↓
ChromaDB
```

### Production Query Flow

```text
User Question
    ↓
Guardrails
    ↓
BM25 Retrieval
    ↓
Top Relevant Chunks
    ↓
Groq LLM
    ↓
Answer + Source Link
```

The project contains an offline embedding and ChromaDB pipeline for the RAG indexing workflow.

The deployed production application uses BM25 retrieval because it provides a lightweight retrieval layer suitable for the available Render runtime memory.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| LLM | Groq — `openai/gpt-oss-20b` |
| Production Retrieval | BM25 — `rank-bm25` |
| Vector Database | ChromaDB |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Data Collection | Requests + BeautifulSoup |
| Environment Management | python-dotenv |
| Deployment | Render |
| Version Control | Git + GitHub |

## Project Structure

```text
mutual-fund-rag-chatbot/
│
├── data/
│   ├── raw/
│   └── chunks/
│
├── docs/
│   ├── sources.md
│   ├── sample_qa.md
│   └── disclaimer.md
│
├── src/
│   ├── app.py
│   ├── collect_sources.py
│   ├── chunk_sources.py
│   ├── embed_store.py
│   ├── guardrails.py
│   ├── rag_pipeline.py
│   └── retriever.py
│
├── tests/
│   └── evaluate.py
│
├── .env.example
├── .gitignore
├── ProblemStatement.txt
├── README.md
└── requirements.txt
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit `.env` or expose the API key.

### 5. Run the application

```bash
streamlit run src/app.py
```

The application will open in the browser.

## Source List

The chatbot currently uses five public scheme pages:

1. **HDFC Large Cap Fund Direct Growth**  
   https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

2. **HDFC Equity Fund Direct Growth**  
   https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth

3. **HDFC ELSS Tax Saver Fund Direct Plan Growth**  
   https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth

4. **HDFC Small Cap Fund Direct Growth**  
   https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth

5. **HDFC Balanced Advantage Fund Direct Growth**  
   https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth

A detailed source list is also available in `docs/sources.md`.

## Sample Q&A

### Q1. What is the expense ratio of HDFC Large Cap Fund Direct Growth?

**Answer:** The expense ratio for the HDFC Large Cap Fund Direct Growth is 1.03%.

**Source:**  
https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

---

### Q2. What is the minimum SIP investment for HDFC Large Cap Fund Direct Growth?

**Answer:** The minimum SIP investment is ₹100.

**Source:**  
https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

---

### Q3. What is the exit load of HDFC Large Cap Fund Direct Growth?

**Answer:** An exit load of 1% applies if the units are redeemed within 1 year.

**Source:**  
https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

---

### Q4. What is the benchmark of HDFC Small Cap Fund Direct Growth?

**Answer:** The benchmark is the BSE 250 SmallCap Total Return Index.

**Source:**  
https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth

---

### Q5. What is the minimum SIP investment for HDFC Balanced Advantage Fund Direct Growth?

**Answer:** The minimum SIP investment is ₹100.

**Source:**  
https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth

---

### Unsupported question example

**Question:** What is the expense ratio of SBI Small Cap Fund?

**Answer:** I don't know based on the available sources.

**Source:** No source is displayed because the fund is not covered by the current knowledge base.

## Guardrails

The chatbot:

- Answers factual questions about supported schemes.
- Refuses investment advice and recommendations.
- Refuses unrelated questions.
- Refuses questions about unsupported funds.
- Does not provide future return predictions.
- Does not provide buy/sell recommendations.
- Returns an "I don't know" response when the available sources do not contain enough information.

## Disclaimer

> **Facts-only. No investment advice.**

This chatbot provides factual information from its available knowledge base. It does not provide investment recommendations, buy/sell advice, portfolio recommendations, or predictions of future returns.

The information provided by the chatbot should not be considered financial advice. Users should refer to the original source documents for the latest information and make their own decisions.

The complete disclaimer is also available in `docs/disclaimer.md`.

## Evaluation

The project includes an automated evaluation script:

```bash
python tests/evaluate.py
```

Current evaluation result:

```text
8/8 tests passed
```

The evaluation covers:

- Factual retrieval
- Expected factual values
- Source URL validation
- Investment-advice refusal
- Unsupported-fund refusal

## Deployment

The application is deployed on Render.

Production start command:

```bash
streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0
```

The application automatically redeploys when changes are pushed to the GitHub repository.

## Production Validation

The deployed application has been manually tested for:

- Expense ratio retrieval
- Minimum investment retrieval
- Exit load retrieval
- Source link generation
- Investment advice refusal
- Unsupported fund refusal
- No misleading source for unsupported questions

### Example

Question:

```text
What is the expense ratio of HDFC Large Cap Fund Direct Growth?
```

Answer:

```text
The expense ratio for the HDFC Large Cap Fund Direct Growth is 1.03%.
```

The response includes the relevant source link.

## Limitations

- The chatbot only answers questions covered by its current knowledge base.
- The current corpus contains five scheme sources.
- It does not provide investment recommendations.
- It does not predict future returns.
- It does not compare investment performance.
- It does not accept or store personal financial information.
- Source information is limited to the available source pages.
- The production deployment currently uses BM25 retrieval rather than running the embedding and ChromaDB pipeline at runtime.

## Security

- API keys are stored in environment variables.
- `.env` is excluded from Git.
- `.env.example` contains placeholders only.
- No PAN, Aadhaar, OTP, phone number, email, or account information is collected or stored.

## Project Status

```text
Prototype                    Complete
Data ingestion               Complete
Chunking                     Complete
Retrieval                    Complete
Groq integration             Complete
Guardrails                   Complete
Streamlit UI                 Complete
Source citations             Complete
Automated evaluation         8/8 passed
Render deployment            Complete
Documentation               Complete
```

## Future Improvements

Potential future improvements include:

- Expanding the source corpus.
- Adding more official AMC, SEBI, and AMFI sources.
- Introducing hybrid BM25 + vector retrieval.
- Improving citation handling.
- Adding more automated evaluation cases.
- Adding source freshness tracking.
