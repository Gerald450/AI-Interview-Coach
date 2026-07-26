# AI Interview Coach

A learning project where I'm building the foundations of an AI interview coach from scratch — synthetic dataset generation, data cleaning, embeddings, and semantic search.

The long-term goal is a system that can retrieve relevant interview Q&A and (eventually) coach someone through answers. Right now I'm focused on the retrieval stack: generate data → clean it → embed it → search it.

---

## Why this project?

I'm preparing for AI engineering roles and wanted something hands-on that touches the pieces I keep seeing in job descriptions:

- Working with LLMs locally (Ollama)
- Structured outputs + validation (Pydantic)
- Synthetic dataset pipelines
- Embedding models and vector similarity search (FAISS)
- Messy real-world data cleaning (because LLMs don't always return clean JSON)

This repo is me learning those pieces by building them, not just reading about them.

---

## What it does today

### 1. Generate interview Q&A with a local LLM

Inside `Interview_dataset_pipeline/`, a small pipeline prompts **Ollama** (`llama3.2:1b`) to generate interview examples across categories like DSA, system design, ML/AI, behavioral, DevOps, etc.

Each example looks roughly like:

```json
{
  "id": 3,
  "question": "What is the primary difference between a private and public IP address...",
  "answer": "A private IP address is used within a local network...",
  "difficulty": "easy",
  "category": "Networking",
  "company": null,
  "tags": ["networking", "private/public ip"],
  "created_at": "..."
}
```

Examples are appended to `Interview_dataset_pipeline/datasets/raw/interviews.jsonl`.

### 2. Clean noisy LLM output

Small models sometimes wrap questions in JSON, invent placeholder tags (`tag1`, `tag2`), or return broken answers. Cleaning happens in two places:

- **On write:** `JSONLWriter` filters bad rows before they land in the dataset
- **Batch cleanup:** `cleanJsonl.py` rewrites an existing JSONL file (with a backup)

### 3. Embed questions + build a FAISS index

`embed.py` loads the dataset, embeds each question with **BAAI/bge-base-en-v1.5** via Sentence Transformers, then builds a FAISS `IndexFlatIP` (inner product on normalized vectors ≈ cosine similarity).

Outputs:

- `embeddings.npy`
- `metadata.json`
- `interview.index`

### 4. Test retrieval

`testRetrival.py` encodes a query, searches the FAISS index, and prints the top-k similar interview questions. Early proof that semantic search over the dataset actually works.

---

## Project layout

```
AI-Interview-Coach/
├── Interview_dataset_pipeline/   # synthetic data generation pipeline
│   ├── main.py                   # generate N interview examples
│   ├── app/
│   │   ├── config.py             # categories, difficulties, target size
│   │   ├── models/               # Pydantic schemas (InterviewExample, enums)
│   │   ├── generators/           # prompts, Ollama client, retry logic
│   │   └── storage/              # JSONL writer + inline cleaning
│   └── datasets/raw/
│       └── interviews.jsonl
├── cleanJsonl.py                 # batch cleaner for existing JSONL
├── embed.py                      # embed questions + write FAISS index
└── testRetrival.py               # quick semantic search smoke test
```

---

## Tech stack

| Piece | What I'm using | Why |
| --- | --- | --- |
| Local LLM | Ollama + `llama3.2:1b` | Free, offline, good for iterating on data gen |
| Schema / validation | Pydantic | Keep generated examples structured |
| Embeddings | `BAAI/bge-base-en-v1.5` | Solid open embedding model for retrieval |
| Vector search | FAISS (`IndexFlatIP`) | Fast similarity search over question embeddings |
| Dataset format | JSONL | Easy to append, stream, and inspect line-by-line |

---

## Setup

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running
- Pull the generation model:

```bash
ollama pull llama3.2:1b
```

### Install dependencies

From `Interview_dataset_pipeline/`:

```bash
python -m venv interview_coach
source interview_coach/bin/activate   # Windows: interview_coach\Scripts\activate
pip install -r requirements.txt
```

For embedding / retrieval (root scripts), you'll also want:

```bash
pip install sentence-transformers faiss-cpu numpy rich
```

---

## Usage

### Generate interview examples

```bash
cd Interview_dataset_pipeline
python main.py
```

This generates examples into `datasets/raw/interviews.jsonl` (batch size is controlled in `main.py` via `CUSTOM_TARGET`).

### Clean an existing JSONL file

```bash
# expects interviews.jsonl in the current directory
python cleanJsonl.py
```

Creates `interviews_backup.jsonl`, then rewrites the cleaned dataset.

### Build embeddings + FAISS index

```bash
python embed.py
```

### Try semantic search

```bash
python testRetrival.py
```

Edit the `query` list in that file to try your own questions.

---

## Pipeline flow

```
Ollama (llama3.2:1b)
        │
        ▼
 InterviewGenerator  ──►  JSONLWriter (clean on write)
        │
        ▼
 interviews.jsonl
        │
        ├──► cleanJsonl.py (optional batch cleanup)
        │
        ▼
     embed.py
   (BGE embeddings)
        │
        ▼
 FAISS index + metadata
        │
        ▼
 testRetrival.py  (top-k similar questions)
```

---

## What's next

Things I still want to build toward a real coach:

- [ ] Better generation quality (stronger model / better prompts / stricter validators)
- [ ] Deduplication and quality scoring on the dataset
- [ ] Wire retrieval into an actual RAG answer / coaching loop
- [ ] Filter by difficulty, category, or company at query time
- [ ] Simple CLI or web UI for practice sessions
- [ ] Evaluation: does retrieved context actually help answer quality?

---

## Notes / caveats

- This is a **work-in-progress learning project**, not a polished product.
- Generated answers vary in quality — especially with a small local model. Cleaning helps, but the dataset still needs more filtering and evaluation.
- Large artifacts (`*.jsonl`, `*.npy`, `*.index`, `metadata.json`) are gitignored on purpose.

If you're also learning AI engineering: clone it, break it, regenerate data, and poke at the retrieval results. That's kind of the point.
