import os
import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "").rstrip("/")
KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")

if not ENDPOINT or not KEY or not REGION:
    missing = [k for k in ["AZURE_TRANSLATOR_ENDPOINT","AZURE_TRANSLATOR_KEY","AZURE_TRANSLATOR_REGION"] if not os.getenv(k)]
    raise RuntimeError(f"Variáveis ausentes: {', '.join(missing)}")

app = FastAPI(title="Azure Translator Demo")

@app.get("/", response_class=HTMLResponse)
def home():
    return """<h2>Azure Translator Demo</h2>
<form action="/translate">
  <input name="text" placeholder="Digite um texto" style="width:300px">
  <input name="to" value="en">
  <button>Traduzir</button>
</form>
<p>Ou abra <a href="/static/index.html">/static/index.html</a></p>
"""

@app.get("/translate")
def translate(text: str = Query(..., min_length=1), to: str = Query("en"), source: str | None = Query(None)):
    params = {"api-version": "3.0", "to": to}
    if source: params["from"] = source
    url = f"{ENDPOINT}/translate"
    headers = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-Type": "application/json"
    }
    body = [{"Text": text}]
    try:
        r = requests.post(url, params=params, headers=headers, json=body, timeout=10)
        r.raise_for_status()
        data = r.json()
        # pega a primeira tradução
        translated = data[0]["translations"][0]["text"]
        return {"text": text, "to": to, "translation": translated, "raw": data}
    except requests.HTTPError as e:
        raise HTTPException(status_code=r.status_code, detail=r.text) from e
