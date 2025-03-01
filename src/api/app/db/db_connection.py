import re
from loguru import logger
import psycopg2
from fastapi import FastAPI, Depends, Query, HTTPException
from core.config import (
    POSTGRES_SERVER,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PORT,
    POSTGRES_PASSWORD,
)


class DbConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=POSTGRES_SERVER,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        logger.info("Db connection established")

    def sanitize_query(self, query: str) -> str:
        """
        Ensures the model-generated query does not already contain LIMIT/OFFSET.
        If it does, enforce a maximum limit of 5000.
        """
        query_lower = query.lower()

        # Ensure the query is a SELECT statement
        if not query_lower.startswith("select"):
            raise HTTPException(
                status_code=400, detail="Only SELECT queries are allowed"
            )

        # Check for existing LIMIT clause
        if "limit" in query_lower:
            match = re.search(r"limit\s+(\d+)", query_lower)
            if match:
                user_limit = int(match.group(1))
                if user_limit > 5000:  # Enforce max limit
                    query = re.sub(
                        r"limit\s+\d+", f"LIMIT 5000", query, flags=re.IGNORECASE
                    )
            return query  # Return query with existing LIMIT

        return query  # Return sanitized query without pagination

    def execute_query(self, query_id, paginated_query, limit=None, offset=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(paginated_query, (limit, offset))
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]  # Get column names

            return {
                "query_id": query_id,
                "data": [dict(zip(columns, row)) for row in rows],
                "limit": limit,
                "offset": offset,
            }

        except Exception as e:
            return {"error": str(e)}