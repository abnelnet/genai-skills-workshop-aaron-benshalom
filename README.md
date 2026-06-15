# GenAI Skills Workshop — Aaron Ben-Shalom

Solutions for the **Public Sector GenAI Delivery Excellence — Skills Validation Workshop**
(Google Cloud). Five challenges building toward a secure, production-quality generative-AI agent,
implemented entirely on Google Cloud (Vertex AI / Gemini, Model Armor, BigQuery, the Evaluation
service, and AI Applications).

## Challenges

|#|Challenge                                     |Focus                                                            |Status    |File                       |
|-|----------------------------------------------|-----------------------------------------------------------------|----------|-----------------------------|
|1|Gemini Prompt Security                        |Secure coding/IT chatbot with Model Armor + Gemini safety filters| Complete |[`challenge1`](./challenge-1-aaron.ipynb)|
|2|RAG in BigQuery                               |Embeddings + vector search over the Aurora Bay FAQs              | Complete |[`challenge2`](./challenge-2-aaron.ipynb)|
|3|Testing & Evaluation                          |Gemini functions, pytest unit tests, Evaluation API              | Complete |[`challenge3`](./challenge-3-aaron.ipynb)|
|4|Agents with AI Applications *(bonus)*         |Conversational Agent with Playbook + Data Store                  | Complete |[`challenge4`](./challenge-4/challenge-4-aaron.md)|
|5|Alaska Dept. of Snow Online Agent *(capstone)*|Production RAG agent deployed to a website                       | Planned |[`challenge5`](./challenge-5/challenge-5-aaron.ipynb)|

## Summaries

**Challenge 1 — Gemini Prompt Security.** A coding & IT chatbot on the latest Gemini, with Model
Armor screening both the user input (`input-prompt-template`) and the model output
(`output-prompt-template`, including Sensitive Data Protection), plus Gemini’s built-in safety
filters and response validation.

**Challenge 2 — RAG in BigQuery.** Load the Aurora Bay FAQs
(`gs://labs.roitraining.com/aurora-bay-faqs/aurora-bay-faqs.csv`) into BigQuery, generate
embeddings per Q&A pair with `ML.GENERATE_EMBEDDING`, retrieve with `VECTOR_SEARCH`, and pass the
matches + question to Gemini for a grounded answer.

**Challenge 3 — Testing & Evaluation.** A Gemini question-classifier (Employment / General
Information / Emergency Services / Tax Related) and a government social-post generator, covered by
`pytest` unit tests and compared across prompts with the Google Evaluation API.

**Challenge 4 — Agents with AI Applications (bonus).** An “Aurora Bay Agent” Conversational Agent
(US-Central1) with a Default Playbook and a Data Store backed by
`gs://labs.roitraining.com/aurora-bay-faqs`

**Challenge 5 — Alaska Dept. of Snow Online Agent (capstone).** A secure, deployed RAG agent over
`gs://labs.roitraining.com/alaska-dept-of-snow`: backend data store + API, unit tests, evaluation
data, prompt filtering and response validation, full prompt/response logging, a solution diagram,
and a website deployment.

## Environment

- **Notebooks** run in Agent Platform **Colab Enterprise** (Application Default Credentials — no keys).
- **Region:** Model Armor templates in `us-east1`; Gemini via the `global` endpoint; AI Applications
  in `us-east1`.
- **Project** is resolved at runtime so each notebook is portable across GCP projects.

## Grading

Each challenge contains its runnable artifact (notebook / agent export / diagram). Notebooks are committed **with their cell outputs** so results are visible without
re-running.
