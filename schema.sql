-- Enable the pgvector extension (provides the `vector` column type + similarity operators)
CREATE EXTENSION IF NOT EXISTS vector;

-- One row per uploaded file
CREATE TABLE IF NOT EXISTS documents (
    id          SERIAL PRIMARY KEY,
    filename    TEXT NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- One row per chunk of a document, with its embedding.
-- Dimension 384 matches the all-MiniLM-L6-v2 embedding model used in rag.py.
-- If you swap embedding models, update this dimension to match.
CREATE TABLE IF NOT EXISTS chunks (
    id           SERIAL PRIMARY KEY,
    document_id  INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index  INTEGER NOT NULL,
    content      TEXT NOT NULL,
    embedding    vector(384) NOT NULL
);

-- IVFFlat index for fast approximate nearest-neighbor search (cosine distance).
-- `lists` is a tuning knob — 100 is a reasonable default for small/medium corpora.
-- Note: IVFFlat indexes are more effective once the table has some data in it;
-- for tiny dev datasets a plain sequential scan is fine too.
CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX IF NOT EXISTS chunks_document_id_idx ON chunks(document_id);
