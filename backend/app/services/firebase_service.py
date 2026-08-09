"""Persistence adapter used by the business services.

The original project contained a Firebase placeholder that never saved data.
For a hackathon demo we use SQLite by default, so the app works without cloud
credentials and survives server restarts.  The public methods intentionally
keep the original Firebase-like interface so the rest of the project stays
simple and a Firestore implementation can be swapped in later.
"""

import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.config import settings


class FirebaseService:
    def __init__(self, database_path: Optional[str] = None):
        self.database_path = database_path or settings.DATABASE_PATH
        self.connected = False
        self.lock = threading.RLock()
        self.connect()

    def _connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def connect(self):
        try:
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
            with self._connection() as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS documents (
                        collection TEXT NOT NULL,
                        document_id TEXT NOT NULL,
                        payload TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        PRIMARY KEY (collection, document_id)
                    )
                    """
                )
                connection.execute(
                    "CREATE INDEX IF NOT EXISTS idx_documents_collection "
                    "ON documents(collection)"
                )
            self.connected = True
        except (OSError, sqlite3.Error):
            self.connected = False
            raise
        return self.connected

    @property
    def enabled(self) -> bool:
        return self.connected

    def get_document(
        self,
        collection: str,
        document_id: str
    ) -> Optional[dict]:
        with self.lock, self._connection() as connection:
            row = connection.execute(
                "SELECT payload FROM documents "
                "WHERE collection = ? AND document_id = ?",
                (collection, document_id),
            ).fetchone()

        if not row:
            return None

        document = json.loads(row["payload"])
        document.setdefault("id", document_id)
        return document

    def get_collection(self, collection: str) -> list[dict]:
        with self.lock, self._connection() as connection:
            rows = connection.execute(
                "SELECT document_id, payload FROM documents "
                "WHERE collection = ? ORDER BY updated_at DESC",
                (collection,),
            ).fetchall()

        documents = []
        for row in rows:
            document = json.loads(row["payload"])
            document.setdefault("id", row["document_id"])
            documents.append(document)
        return documents

    def add_document(
        self,
        collection: str,
        data: dict
    ) -> str:
        document = dict(data)
        document_id = str(document.get("id") or uuid.uuid4())
        document["id"] = document_id
        now = datetime.now(timezone.utc).isoformat()

        with self.lock, self._connection() as connection:
            connection.execute(
                """
                INSERT INTO documents
                    (collection, document_id, payload, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    collection,
                    document_id,
                    json.dumps(document, ensure_ascii=False),
                    now,
                    now,
                ),
            )
        return document_id

    def update_document(
        self,
        collection: str,
        document_id: str,
        data: dict
    ) -> Optional[dict]:
        with self.lock:
            current = self.get_document(collection, document_id)
            if current is None:
                return None

            current.update(data)
            current["id"] = document_id
            now = datetime.now(timezone.utc).isoformat()

            with self._connection() as connection:
                connection.execute(
                    "UPDATE documents SET payload = ?, updated_at = ? "
                    "WHERE collection = ? AND document_id = ?",
                    (
                        json.dumps(current, ensure_ascii=False),
                        now,
                        collection,
                        document_id,
                    ),
                )
            return current

    def delete_document(
        self,
        collection: str,
        document_id: str
    ) -> bool:
        with self.lock, self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM documents "
                "WHERE collection = ? AND document_id = ?",
                (collection, document_id),
            )
        return cursor.rowcount > 0

    def clear_collection(self, collection: str) -> int:
        with self.lock, self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM documents WHERE collection = ?",
                (collection,),
            )
        return cursor.rowcount


firebase_service = FirebaseService()
