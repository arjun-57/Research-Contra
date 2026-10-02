# Contra: A Research Team That Argues With Itself

> **Treat research like a court trial, not a search engine.**  
> Rather than summarizing agreeable consensus from the web, Contra convenes an adversarial courtroom where opposing agents cross-examine claims, execute real code on statutory datasets, and deliver a calibrated verdict with explicit falsification conditions ("What would change my mind").

---

## 🏛️ Architecture Overview

```
                         ┌────────────┐
                         │    User    │
                         └─────┬──────┘
                               ▼
                    ┌─────────────────────┐
                    │   Question Framer   │  ← Operationalizes terms, metrics & falsification criteria
                    └─────────┬───────────┘
                              ▼
                    ┌─────────────────────┐
                    │   Manager Agent     │  ← Pre-registers trial protocol & orchestrates pipeline
                    └─────────┬───────────┘
          ┌───────────────┬───┴───────────┬────────────────┐   PARALLEL
          ▼               ▼               ▼                ▼
   ┌────────────┐  ┌─────────────┐  ┌───────────┐  ┌──────────────┐
   │ Web Agent  │  │ Data Agent  │  │ RAG Agent │  │Source Auditor│
   │ dialectical│  │ sandbox math│  │ user docs │  │scores bias & │
   │ retrieval  │  │ second deriv│  │ + cache   │  │credibility   │
   └─────┬──────┘  └──────┬──────┘  └─────┬─────┘  └───────┬──────┘
         └────────────────┴───────┬───────┴────────────────┘
                                  ▼
                     ╔═════════════════════════╗
                     ║     EVIDENCE LEDGER     ║  ← Single source of truth, Bayesian scoring
                     ╚════════════╤════════════╝
                       ┌──────────┴──────────┐
                       ▼                     ▼
                ┌─────────────┐       ┌─────────────┐
                │   Advocate  │       │   Skeptic   │  ← Adversarial trial debate
                └──────┬──────┘       └──────┬──────┘
                       └──────────┬──────────┘
                                  ▼
                        ┌──────────────────┐
                        │  Cross-Examiner  │  ← Deposition interrogatories & judge rulings
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │   Fact Checker   │  ← Verifies claim correspondence
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │  Report Writer   │  ← Synthesizes calibrated verdict & "What Would Change My Mind"
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │ Citation Auditor │  ← Strikes any statement lacking ledger verification
                        └────────┬─────────┘
                                 ▼
                         Calibrated Verdict
```

---

## 🔑 API Keys & SDK Integration

Contra is built using the official **Google GenAI SDK** (`google-genai`):

### 1. Setting Up Your API Key
Set your Gemini API key in your environment or in `contra/.env`:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Optionally, you can also provide `TAVILY_API_KEY` for live web search).*

> **Note:** Contra contains a built-in empirical sandbox fallback engine, so the entire pipeline runs seamlessly even before an API key is entered!

### 2. Official Google GenAI SDK Usage
In `contra/app/core/llm.py`, Contra integrates with `google-genai`:

```python
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Structured JSON Generation for Adversarial Agents
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

## 🚀 Quickstart & Running

### 1. Backend (FastAPI + Server-Sent Events)
```bash
cd contra
# Activate virtual environment
.\.venv\Scripts\activate
# Start backend on port 8000
uvicorn contra.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### 2. Frontend (Next.js Dashboard)
```bash
cd contra/web
npm run dev
```
Open `http://localhost:3000` to interact with the trial courtroom.

### 3. Run Automated Tests
```bash
cd contra
.\.venv\Scripts\python.exe -m pytest tests -v
```

### 4. Run Adversarial Benchmark Evaluation Suite
```bash
cd contra
.\.venv\Scripts\python.exe evals/benchmark_evals.py
```
