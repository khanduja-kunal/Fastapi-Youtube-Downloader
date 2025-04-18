from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.download import router as download_router
from app.api.metadata import router as metadata_router
from app.api.history import router as history_router

# FastAPI App
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(download_router)
app.include_router(metadata_router)
app.include_router(history_router)
