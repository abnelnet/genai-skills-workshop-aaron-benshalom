# Challenge Five — Architecture

Solution diagram and requirement mapping for the Alaska Department of Snow online agent. Backend is
`challenge-5-aaron.ipynb`; the deployable service is `main.py` + `index.html`.

```mermaid
flowchart LR
    U["Website / user"] -->|question| API["FastAPI on Cloud Run"]
    API --> IN["Model Armor input screen"]
    IN -->|blocked| REF["Refusal"] --> LOG
    IN -->|clean| RET["BigQuery RAG: VECTOR_SEARCH over faqs_embedded"]
    RET --> GEN["Gemini (grounded, context-only)"]
    GEN --> OUT["Model Armor output screen (+ SDP)"]
    OUT -->|bad| ERR["Safe error"] --> LOG
    OUT -->|ok| ANS["Grounded answer"] --> LOG
    ANS --> API
    LOG["interaction_log (BigQuery)"]
    EVAL["Gen AI Evaluation Service (offline)"] -. scores .-> RET
```

## Requirement -> implementation
| Requirement | Implementation |
|---|---|
| Backend data store for RAG | Snow FAQs in BigQuery, embedded with `ML.GENERATE_EMBEDDING`, retrieved with `VECTOR_SEARCH` (Challenge 2) |
| Backend API functionality | `answer()` exposed via FastAPI `/ask` on Cloud Run (`main.py`) |
| Prompt filtering & response validation | Model Armor input + output templates (Challenge 1) |
| Log all prompts and responses | `interaction_log` BigQuery table |
| Unit tests | `pytest` via `ipytest` (grounding, injection, retrieval) |
| Evaluation data | `EvalTask` groundedness + instruction-following (Challenge 3) |
| Deployed to a website | Cloud Run service + `index.html` front end |

## Deploy
From the `challenge-5/` directory (which holds `main.py`, `requirements.txt`, `Procfile`):
```
gcloud run deploy snow-agent --source . --region us-central1 --allow-unauthenticated
```
Paste the service URL into `index.html` (`BASE`) and host the page (Cloud Storage static site, or
open locally to test).
