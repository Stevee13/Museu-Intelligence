import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.models import Opportunity

DEFAULT_DB_PATH = "data/museu.db"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                agency_name TEXT NOT NULL,
                source_url TEXT NOT NULL UNIQUE,
                submission_deadline TEXT,
                max_budget REAL,
                score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 5),
                justification TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_opportunity(opportunity: Opportunity, db_path: str = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO opportunities (id, title, agency_name, source_url, submission_deadline, max_budget, score, justification)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_url) DO UPDATE SET
                title=excluded.title,
                agency_name=excluded.agency_name,
                source_url=excluded.source_url,
                submission_deadline=excluded.submission_deadline,
                max_budget=excluded.max_budget,
                score=excluded.score,
                justification=excluded.justification
            """,
            (
                opportunity.id,
                opportunity.title,
                opportunity.agency_name,
                opportunity.source_url,
                opportunity.submission_deadline.isoformat() if opportunity.submission_deadline else None,
                opportunity.max_budget,
                opportunity.score,
                opportunity.justification,
            ),
        )
        conn.commit()


def get_opportunities(
    min_score: Optional[int] = None, db_path: str = DEFAULT_DB_PATH
) -> List[Opportunity]:
    query = "SELECT * FROM opportunities"
    params = []

    if min_score is not None:
        query += " WHERE score >= ?"
        params.append(min_score)

    query += " ORDER BY score DESC, created_at DESC"

    with get_connection(db_path) as conn:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()

    return [
        Opportunity(
            id=row["id"],
            title=row["title"],
            agency_name=row["agency_name"],
            source_url=row["source_url"],
            submission_deadline=datetime.fromisoformat(row["submission_deadline"]) if row["submission_deadline"] else None,
            max_budget=row["max_budget"],
            score=row["score"],
            justification=row["justification"],
        )
        for row in rows
    ]
    