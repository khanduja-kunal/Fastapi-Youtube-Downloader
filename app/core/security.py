from app.core.config import API_KEY
from fastapi import Header, HTTPException, status

if not API_KEY:
    raise ValueError("API_KEY is missing from environment variables.")

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key."
        )
    return x_api_key
