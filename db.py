"""
Database access layer — Postgres with the pgvector extension.

Replaces a dedicated vector store (Chroma/Pinecone/etc.) with plain SQL:
documents and their chunk embeddings live in normal Postgres tables, and
similarity search uses pgvector's `<=>` cosine-distance operator.
"""

import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://rag_user:rag_password@localhost:5432/rag_db",
)


@contextmanager
def get_conn():
    """Yield a connection with pgvector types registered, committing on success."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        register_vector(conn)
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_document(filename: str) -> int:
    """Create a document row, return its id."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents (filename) VALUES (%s) RETURNING id",
                (filename,),
            )
            return cur.fetchone()[0]


def insert_chunks(document_id: int, chunks: list[str], embeddings: list[list[float]]):
    """Bulk-insert chunk rows with their embeddings."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            rows = [
                (document_id, i, chunk, embedding)
                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
            ]
            psycopg2.extras.execute_values(
                cur,
                "INSERT INTO chunks (document_id, chunk_index, content, embedding) VALUES %s",
                rows,
                template="(%s, %s, %s, %s)",
            )


def similarity_search(query_embedding: list[float], top_k: int = 4) -> list[dict]:
    """
    Return the top_k chunks closest to query_embedding by cosine distance,
    joined with their source document's filename.
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT c.content,
                       d.filename AS source,
                       1 - (c.embedding <=> %s) AS score
                FROM chunks c
                JOIN documents d ON d.id = c.document_id
                ORDER BY c.embedding <=> %s
                LIMIT %s
                """,
                (query_embedding, query_embedding, top_k),
            )
            return list(cur.fetchall())


def list_sources() -> list[dict]:
    """Return each document with its chunk count, most recent first."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT d.filename, d.uploaded_at, COUNT(c.id) AS chunk_count
                FROM documents d
                LEFT JOIN chunks c ON c.document_id = d.id
                GROUP BY d.id
                ORDER BY d.uploaded_at DESC
                """
            )
            return list(cur.fetchall())


def has_any_chunks() -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT EXISTS (SELECT 1 FROM chunks LIMIT 1)")
            return cur.fetchone()[0]


def clear_all():
    """Wipe all documents and chunks (cascades)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE documents, chunks RESTART IDENTITY CASCADE")
