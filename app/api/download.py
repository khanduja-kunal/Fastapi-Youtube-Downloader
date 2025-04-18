from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from celery import Celery
from app.db.models import DownloadRequest
from app.utils.validation import is_valid_youtube_url
from app.core.rate_limit import check_rate_limit
from app.db.session import get_session
from app.core.security import get_api_key
from app.utils.validation import validate_video_constraints


router = APIRouter()

celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']


@router.post("/download/")
async def download_trigger(
    request: DownloadRequest,
    user_api_key: str = Depends(get_api_key),
    client: Request = None,
    session: AsyncSession = Depends(get_session)
):
    client_ip = client.client.host
    check_rate_limit(client_ip)

    if not is_valid_youtube_url(request.url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid YouTube URL.")
    
    if request.format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported format. Allowed: {ALLOWED_FORMATS}")
    if request.quality.lower() not in ALLOWED_QUALITIES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported quality. Allowed: {ALLOWED_QUALITIES}")

    await validate_video_constraints(request.url, session)

    task = celery_app.send_task(
        "app.worker.download_task.download_video_task",
        args=[request.url, request.format.lower(), request.quality.lower()],
    )
    return {"task_id": task.id, "message": "Download started"}
