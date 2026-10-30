# Vectra ✦

**An evidence-first RAG workspace: upload your documents, ask questions, and get answers with citations you can check.**

Vectra is a Retrieval-Augmented Generation (RAG) app built with Streamlit. It extracts text from your files, indexes it with sentence embeddings, retrieves the passages closest to your question, and asks a language model to answer **only from that evidence**, citing the document and page for every claim. It can run fully locally (Ollama), so private documents never have to leave your machine.

> Built as a B.Tech Computer Science mini project (AKTU, Lloyd Institute of Engineering & Technology).

---

## Features

- **Multi-format ingestion**: PDF, DOCX, TXT and Markdown, with page-level source locations for PDFs
- **Semantic search**: `all-MiniLM-L6-v2` embeddings (384-dim) with cosine similarity
- **Cited answers**: numbered citations `[1]`, `[2]` tied to document, page and similarity score
- **Honest failure handling**: tells you when evidence is insufficient or conflicting, and shows the retrieved passages if the model is offline
- **Insight Lab**: compares two or more documents (summaries, similarities, differences, possible contradictions, limitations). Passages are retrieved from each document separately so every source is represented fairly
- **Trust & Evaluation page**: test retrieval on questions with known answers and work through an evaluation checklist
- **Prompt-injection awareness**: document text is treated as untrusted data in every prompt
- **Local-first**: runs with Ollama, with no API costs and no data leaving your machine
- **Re-upload safe**: uploading a file again replaces its old index entries instead of duplicating them

## How it works

```
Upload → Extract text (with page) → Chunk (180 words, 35 overlap) → Embed → Local index
                                                                          │
Question → Embed → Top-k cosine search ─────────────────────────────────┘
                        │
                        └→ Prompt with numbered evidence → Ollama → Cited answer + sources
```

## Tech stack

| Area | Technology |
| --- | --- |
| UI | Streamlit |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector search | NumPy (local JSON index) |
| LLM | Ollama (`llama3.2` by default) |
| Parsing | pypdf, python-docx |
| Optional storage layer | PostgreSQL + pgvector (`db.py`, `schema.sql`) |

## Getting started

### Prerequisites

- Python 3.10+ (developed on 3.13)
- [Ollama](https://ollama.com) installed and running

### Installation

```bash
git clone https://github.com/Wildfrost-stack/VECTRA.git
cd VECTRA

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
ollama pull llama3.2
```

### Run

```bash
streamlit run main.py
```

Open the Knowledge Hub at the top of the page, upload documents, click **Index documents**, then head to **Ask Vectra**.

> The first run downloads the embedding model, so it needs an internet connection and takes a little longer.

## Configuration

Settings are read from environment variables (or a `.env` file). Copy `env.example` to `.env` and edit as needed:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server address |
| `OLLAMA_MODEL` | `llama3.2` | Model used to write answers |
| `OLLAMA_NUM_CTX` | `8192` | Context window requested from Ollama |
| `VECTRA_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |

**Never commit your `.env` file.** It is listed in `.gitignore`.

## Project structure

```
.
├── main.py             # Streamlit app (Overview, Ask Vectra, Insight Lab, Trust & Evaluation)
├── rag_engine.py       # Extraction, chunking, embedding, retrieval, Ollama calls, comparison
├── db.py               # PostgreSQL + pgvector access layer (optional backend storage)
├── schema.sql          # Database tables and IVFFlat index (vector(384))
├── requirements.txt    # Python dependencies
├── env.example         # Configuration template
├── .streamlit/         # Streamlit theme and upload settings
└── vectra_data/        # Created at runtime: index.json (git-ignored)
```

## Optional: PostgreSQL + pgvector storage

`db.py` and `schema.sql` provide a database-backed alternative to the local JSON index: documents and chunk embeddings live in Postgres, and similarity search uses pgvector's `<=>` cosine-distance operator.

```bash
psql "$DATABASE_URL" -f schema.sql
pip install psycopg2-binary pgvector
```

Set `DATABASE_URL` in your `.env`. The Streamlit app uses the local index by default; the database layer is meant for an HTTP backend and is not wired into `main.py`.

## Limitations

- **No OCR**: scanned PDFs without a text layer can't be indexed (Vectra warns you)
- **Text only**: tables, images, charts and formulas aren't interpreted
- **Fixed word-based chunking** and **dense retrieval only** (no keyword/hybrid search or re-ranking)
- **No relevance cut-off**: the nearest passages are always returned, so honesty on unsupported questions depends on the model following the prompt
- **No authentication**: intended for a single user or a trusted environment
- Similarity scores are a ranking, **not** a probability that an answer is correct. Always verify important claims against the original documents

## Roadmap

- [ ] OCR for scanned PDFs
- [ ] Hybrid search (BM25 + embeddings) and cross-encoder re-ranking
- [ ] Minimum similarity threshold
- [ ] Structure-aware chunking
- [ ] Citation verification
- [ ] Authentication and per-user collections
- [ ] Benchmark with a labelled question set (hit rate @k, MRR)

## Screenshots

<!-- Add screenshots here, e.g. ![Overview](docs/overview.png) -->

## Author

**Jitendra Behera**: B.Tech CSE, Lloyd Institute of Engineering & Technology, Greater Noida
Supervisor: Mr. Akshay Kumar, Assistant Professor

## Acknowledgements

[Streamlit](https://streamlit.io), [Sentence-Transformers](https://www.sbert.net), [Ollama](https://ollama.com), [pgvector](https://github.com/pgvector/pgvector), [pypdf](https://pypdf.readthedocs.io) and [python-docx](https://python-docx.readthedocs.io).
