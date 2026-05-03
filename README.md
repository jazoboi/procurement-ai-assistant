# AI-Powered Procurement & SOW Assistant

> Agentic workflow for drafting, validating, and scoring Statement of Work documents against organizational policy.

## Role
**AI Engineer** — Designed the compliance checking pipeline and prompt engineering strategy.

## Overview
Automates the drafting of complex Statement of Work (SOW) documents. The system performs compliance checks against organizational templates, matches relevant clauses, and injects metadata automatically.

## Architecture
```
Template Library → Clause Matcher → SOW Draft Generator
                                          ↓
                      Policy DB → Compliance Checker → Score & Flags
                                          ↓
                                   Final SOW (DOCX/PDF)
```

## Key Features
- **Template-Driven Generation** — Builds SOW sections from organizational templates
- **Clause Matching** — Semantic search across historical SOW clauses (TF-IDF + embeddings)
- **Compliance Scoring** — Validates against 47 policy checkpoints per document
- **Metadata Injection** — Auto-fills contract references, dates, and organizational codes
- **Human-in-the-Loop** — Flags ambiguous sections for manual review

## Tech Stack
`Python` · `NLP` · `Prompt Engineering` · `LangChain` · `python-docx` · `FastAPI`

## Impact
- Cut SOW drafting time from **~5 days to under 30 minutes**
- Achieved **87% compliance score** on first-pass generation
- Reduced legal review cycles by **3x**

## Project Structure
```
src/
├── document_parser.py    # SOW/RFP text extraction
├── compliance_checker.py # Policy validation engine
├── clause_matcher.py     # Semantic clause retrieval
├── sow_generator.py      # Document assembly
└── config.py             # Settings & prompt templates
```

## License
MIT
