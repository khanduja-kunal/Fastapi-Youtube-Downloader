from fastapi import FastAPI
from routes import router as api_router

# Initialize the FastAPI app
app = FastAPI()

# Include the router from routes.py
app.include_router(api_router)
