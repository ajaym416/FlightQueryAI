from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.default_api import router as DefaultApiRouter

app = FastAPI(
    title="Airlines Flight",
    description="Text to Sql",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "OPTIONS", "PATH"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(DefaultApiRouter)
