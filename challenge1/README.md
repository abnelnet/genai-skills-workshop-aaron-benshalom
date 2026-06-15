# Challenge One — Gemini Prompt Security

A secure and safe **coding & IT chatbot** built on the latest Gemini, with guardrails on both the
user input and the model output. Everything runs inside Google Cloud (Vertex AI + Model Armor).

**Author:** Aaron
**Notebook:** [`challenge-1-aaron.ipynb`](./challenge-1-aaron.ipynb)

---

## What it does

A user request is screened, sent to Gemini with a constrained system prompt and safety filters,
and the response is screened again before anything is returned:

```
User -> [input check: Model Armor] -> + system instructions -> Gemini (safety filters)
     -> [output check: Model Armor + SDP] -> OK ? return it : return error
```

The chatbot only answers coding / software / IT questions; anything off-topic gets
`"I can't help with that."`, and unsafe or injected content is blocked at the Model Armor layer.

## Requirements coverage

| # | Requirement | How it's met |
|---|---|---|
| 1 | Python chat app on the latest Gemini | Google Gen AI SDK (Vertex backend); `resolve_model()` selects the newest available model |
| 2 | System instructions with goals + restrictions | `SYSTEM_INSTRUCTIONS` (coding & IT scope, PEP 8, refuse off-topic) |
| 3 | Prompt filtering on user input | `prompt_is_clean()` → Model Armor `input-prompt-template` (prompt injection / jailbreak) |
| 4 | Gemini safety filters | `SAFETY_SETTINGS` (hate / dangerous / sexually-explicit / harassment) on the generate call |
| 5 | Validate responses, return only safe ones | output gate in `secure_chat()` (Gemini `finish_reason` + Model Armor) |
| **Bonus** | Model Armor + Sensitive Data Protection for response filtering | `output-prompt-template` has **SDP = Basic**, enforced inside `sanitizeModelResponse` |

## Defense in depth

Three independent layers, because each catches what the others miss:

1. **System instructions** — enforce *topic scope* (Model Armor does not do this; an off-topic but
   safe request passes its filters cleanly).
2. **Gemini safety filters** — model-native harm-category scoring.
3. **Model Armor** — prompt injection / jailbreak detection on input, and Responsible AI + Sensitive
   Data Protection on output.

## Model Armor templates (region: `us-east1`)

| Template | Prompt injection / jailbreak | Responsible AI | Sensitive Data Protection |
|---|---|---|---|
| `input-prompt-template` | Enabled (Medium and above) | High (all categories) | — |
| `output-prompt-template` | Enabled (Medium and above) | High (all categories) | **Basic (enabled)** |

The notebook recreates these via `ensure_template()` if they don't already exist, so it runs on a
clean project too.

## Prerequisites

- **APIs:** `aiplatform.googleapis.com`, `modelarmor.googleapis.com`
  (Basic SDP on the output template may also require `dlp.googleapis.com`).
- **IAM** for the runtime service account:
  - `roles/aiplatform.user`
  - `roles/modelarmor.admin` (needed only to *create* templates on a fresh project;
    `roles/modelarmor.user` is sufficient once the templates exist).
- Credentials are provided automatically by Colab Enterprise (Application Default Credentials) —
  no API keys or key files.

## How to run

1. Open `challenge-1-aaron.ipynb` in **Agent Platform → Colab Enterprise** (or any Vertex notebook).
2. **Runtime → Run all.**
3. Confirm the demonstration cell at the bottom is populated with output.
4. **File → Download → `.ipynb`** so the saved outputs travel with the notebook.

### Configuration notes

- **Project** is resolved at runtime (ADC / `GOOGLE_CLOUD_PROJECT`) — nothing is hardcoded.
- **Model:** `resolve_model()` tries `gemini-3.1-flash → gemini-2.5-flash → gemini-2.0-flash`.
- **Gemini endpoint** defaults to `global` for the widest model availability; if a model isn't
  served there in your project, set `GENAI_LOCATION` to `us-east1` / `us-central1` and re-run.
- **Model Armor** stays in `us-east1` (`MA_LOCATION`).

## Files

| File | Purpose |
|---|---|
| `challenge-1-aaron.ipynb` | The full solution (documented cells + runnable demo) |
| `README.md` | This file |
