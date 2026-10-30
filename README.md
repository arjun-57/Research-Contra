# Contra: Adversarial Multi-Agent Research Framework

An autonomous multi-agent dialectical research platform that structures inquiries like an adversarial legal trial. Rather than compiling agreeable web summaries, Contra orchestrates competing agents that cross-examine assertions, execute verifiable code in sandbox environments, and deliver calibrated verdicts with explicit falsification thresholds.

---

## Architecture Overview

```
                         ┌────────────┐
                         │    User    │
                         └─────┬──────┘
                               ▼
                    ┌─────────────────────┐
                    │   Question Framer   │  (Operationalizes terms, metrics & criteria)
                    └─────────┬───────────┘
                              ▼
                    ┌─────────────────────┐
                    │   Manager Agent     │  (Pre-registers protocol & orchestrates pipeline)
                    └─────────┬───────────┘
          ┌───────────────┬───┴───────────┬────────────────┐   (Parallel Execution)
          ▼               ▼               ▼                ▼
   ┌────────────┐  ┌─────────────┐  ┌───────────┐  ┌──────────────┐
   │ Web Agent  │  │ Data Agent  │  │ RAG Agent │  │Source Auditor│
   │ dialectical│  │ sandbox math│  │ user docs │  │scores bias & │
   │ retrieval  │  │ second deriv│  │ + cache   │  │credibility   │
   └─────┬──────┘  └──────┬──────┘  └─────┬─────┘  └───────┬──────┘
         └────────────────┴───────┬───────┴────────────────┘
                                  ▼
                     ┌─────────────────────────┐
                     │     EVIDENCE LEDGER     │  (Single source of truth, Bayesian scoring)
                     └────────────┬────────────┘
                       ┌──────────┴──────────┐
                       ▼                     ▼
                ┌─────────────┐       ┌─────────────┐
                │   Advocate  │       │   Skeptic   │  (Adversarial debate & cross-examination)
                └──────┬──────┘       └──────┬──────┘
                       └──────────┬──────────┘
                                  ▼
                        ┌──────────────────┐
                        │  Cross-Examiner  │  (Deposition interrogatories & judge rulings)
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │   Fact Checker   │  (Verifies claim correspondence against ledger)
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │  Report Writer   │  (Synthesizes verdict & falsification criteria)
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │ Citation Auditor │  (Strikes statements lacking ledger backing)
                        └────────┬─────────┘
                                 ▼
                         Calibrated Verdict
```

---

## Core Principles

1. **Adversarial Decomposition**: Inquiries are split into prosecutorial and defensive positions to counter confirmation bias.
2. **Empirical Code Execution**: Statistical claims are independently recomputed via python sandbox execution on underlying raw data.
3. **Falsification Bounds**: Every research verdict specifies empirical conditions under which the hypothesis would be refuted.
4. **Evidence Ledger Integrity**: Only claims with auditable primary-source provenance survive citation auditing.

---

## SDK Integration

Contra is built using the official **Google GenAI SDK** (`google-genai`):

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "system_instruction": "You are the Lead Prosecutorial Skeptic in the Contra research trial."
    }
)
```

---

## Repository Structure

```
.
├── contra/
│   ├── app/                   # FastAPI backend, agent implementations, and core logic
│   │   ├── api/               # REST and Server-Sent Event (SSE) endpoints
│   │   ├── core/              # LLM providers, configuration, and logging
│   │   └── agents/            # Advocate, Skeptic, Cross-Examiner, Auditor
│   ├── evals/                 # Benchmark evaluation suites and test questions
│   ├── tests/                 # Unit and integration tests
│   ├── web/                   # Next.js interactive courtroom dashboard
│   ├── Dockerfile.backend
│   ├── docker-compose.yml
│   └── requirements.txt
└── README.md
```

---

## Setup and Quickstart

### 1. Environment Configuration
```bash
cd contra
cp .env.example .env
# Set your GEMINI_API_KEY in .env
```

### 2. Backend (FastAPI + Server-Sent Events)
```bash
cd contra
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at `http://localhost:8000/docs`.

### 3. Frontend (Next.js Dashboard)
```bash
cd contra/web
npm install
npm run dev
```
Open `http://localhost:3000` to interact with the trial courtroom.

### 4. Running Verification Tests & Evaluations
```bash
cd contra
pytest tests -v
python evals/benchmark_evals.py
```
