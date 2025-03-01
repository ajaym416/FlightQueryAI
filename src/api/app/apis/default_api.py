import uuid
from typing import Dict, Any
from fastapi import APIRouter, FastAPI, Query, HTTPException
from loguru import logger

from app.controller.llm_controller import LLMCaller
from app.db.db_connection import DbConnection

app = FastAPI()
router = APIRouter()
db_connection = DbConnection()

# Dictionary to store generated queries (replace with Redis in production)
query_cache: Dict[str, str] = {}
llm_caller = LLMCaller()


@router.get("/generate_query")
async def generate_and_store_query(
    input_text: str = Query(None, description="Ask me questions about the DB")
):
    """
    Takes a natural language query, converts it to postgresSQL,
    stores the query, and returns a query_id for pagination.
    """

    # Call llm api to generate SQL query
    model_generated_query = llm_caller.generate_sql(input_text)
    # Sanitize query
    sanitized_query = db_connection.sanitize_query(model_generated_query)

    # Generate a unique query_id
    query_id = str(uuid.uuid4())

    # Store query in cache (replace with Redis for production)
    query_cache[query_id] = sanitized_query

    return {"query_id": query_id, "query": sanitized_query}


@router.get("/execute_query")
async def execute_paginated_query(
    query_id: str,
    limit: int = Query(100, ge=1, le=5000),
    offset: int = Query(0, ge=0),
):
    """
    Executes a previously generated query with pagination, without calling the Text2SQL model again.
    """
    logger.info(f"-----------------{query_cache}")
    if query_id not in query_cache:
        raise HTTPException(status_code=404, detail="Query ID not found")

    # Retrieve stored query
    base_query = query_cache[query_id]
    
    # Append pagination
    paginated_query = f"{base_query} LIMIT %s OFFSET %s"
    response  = db_connection.execute_query(query_id=query_id, paginated_query=paginated_query, limit=limit,offset=offset)
    return response
    
    
