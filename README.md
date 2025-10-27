# Azure Translator Demo (FastAPI)

Pequeno serviço que expõe `/translate` usando o **Azure Translator**.

## Pré-requisitos
- Python 3.10+
- Um recurso **Translator** no Azure (pegar `endpoint`, `key`, `region`)

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env   # preencha os valores
uvicorn app:app --reload
