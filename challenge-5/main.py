"""Challenge 5 - Alaska Dept. of Snow agent API (Cloud Run).

Serves the guarded, grounded, logged answer() pipeline over HTTP. Assumes
challenge-5-aaron.ipynb has already built the BigQuery embeddings table
(alaska_snow.faqs_embedded), the remote embedding model, the interaction_log
table, and the Model Armor templates in us-east1.

Deploy (these files + requirements.txt + Procfile in one dir):
    gcloud run deploy snow-agent --source . --region us-central1 --allow-unauthenticated
"""

import datetime
import json
import os
import pathlib

import google.auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from google import genai
from google.api_core.client_options import ClientOptions
from google.cloud import bigquery, modelarmor_v1
from google.genai import types
from pydantic import BaseModel

_creds, _proj = google.auth.default()
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or _proj
BQ_LOCATION, DATASET = "US", "alaska_snow"
MA_LOCATION, GENAI_LOCATION = "us-east1", "global"
EMB_MODEL = f"{PROJECT_ID}.{DATASET}.embedding_model"
EMB_TABLE = f"{PROJECT_ID}.{DATASET}.faqs_embedded"
LOG_TABLE = f"{PROJECT_ID}.{DATASET}.interaction_log"
INPUT_TEMPLATE = (
    f"projects/{PROJECT_ID}/locations/{MA_LOCATION}/templates/input-prompt-template"
)
OUTPUT_TEMPLATE = (
    f"projects/{PROJECT_ID}/locations/{MA_LOCATION}/templates/output-prompt-template"
)
MATCH_FOUND, STRING_COLS = 2, ["question", "answer"]

bq = bigquery.Client(project=PROJECT_ID, location=BQ_LOCATION)
ma = modelarmor_v1.ModelArmorClient(
    transport="rest",
    client_options=ClientOptions(
        api_endpoint=f"modelarmor.{MA_LOCATION}.rep.googleapis.com"
    ),
)
client = genai.Client(vertexai=True, project=PROJECT_ID, location=GENAI_LOCATION)
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
SYS = (
    "You are the Alaska Department of Snow assistant. Answer ONLY from the provided FAQ context. "
    "If the answer is not present, say you don't have that information. Do not invent facts."
)
REFUSAL, ERROR = (
    "I can't help with that.",
    "Sorry - I can't return a safe response to that.",
)


def prompt_is_clean(t):
    r = ma.sanitize_user_prompt(
        modelarmor_v1.SanitizeUserPromptRequest(
            name=INPUT_TEMPLATE, user_prompt_data=modelarmor_v1.DataItem(text=t)
        )
    )
    return int(r.sanitization_result.filter_match_state) != MATCH_FOUND


def response_is_clean(t):
    r = ma.sanitize_model_response(
        modelarmor_v1.SanitizeModelResponseRequest(
            name=OUTPUT_TEMPLATE, model_response_data=modelarmor_v1.DataItem(text=t)
        )
    )
    return int(r.sanitization_result.filter_match_state) != MATCH_FOUND


def retrieve(q, k=3):
    sql = f"""SELECT base.*, distance FROM VECTOR_SEARCH(
      TABLE `{EMB_TABLE}`, 'embedding',
      (SELECT ml_generate_embedding_result AS embedding FROM ML.GENERATE_EMBEDDING(
        MODEL `{EMB_MODEL}`, (SELECT @q AS content),
        STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type))),
      top_k => @k, distance_type => 'COSINE') ORDER BY distance"""
    p = [
        bigquery.ScalarQueryParameter("q", "STRING", q),
        bigquery.ScalarQueryParameter("k", "INT64", k),
    ]
    return [
        dict(r)
        for r in bq.query(
            sql, job_config=bigquery.QueryJobConfig(query_parameters=p)
        ).result()
    ]


def log_interaction(q, bi, bo, rows, resp):
    bq.insert_rows_json(
        LOG_TABLE,
        [
            {
                "ts": datetime.datetime.utcnow().isoformat(),
                "question": q,
                "blocked_input": bi,
                "blocked_output": bo,
                "retrieved": json.dumps([{c: r[c] for c in STRING_COLS} for r in rows]),
                "response": resp,
            }
        ],
    )


def answer(q, k=3):
    bi, rows, bo = not prompt_is_clean(q), [], False
    if bi:
        resp = REFUSAL
    else:
        rows = retrieve(q, k)
        ctx = "\n\n".join("\n".join(f"{c}: {r[c]}" for c in STRING_COLS) for r in rows)
        raw = (
            client.models.generate_content(
                model=MODEL,
                contents=f"FAQ CONTEXT:\n{ctx}\n\nQUESTION: {q}",
                config=types.GenerateContentConfig(
                    system_instruction=SYS, temperature=0.2
                ),
            ).text
            or ""
        ).strip()
        bo = not response_is_clean(raw)
        resp = ERROR if bo else raw
    log_interaction(q, bi, bo, rows, resp)
    return resp


app = FastAPI(title="Alaska Dept. of Snow Agent")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

_INDEX = pathlib.Path(__file__).parent / "index.html"


@app.get("/", response_class=HTMLResponse)
def home():
    return _INDEX.read_text(encoding="utf-8")


class Q(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/ask")
def ask(q: Q):
    return {"answer": answer(q.question)}
