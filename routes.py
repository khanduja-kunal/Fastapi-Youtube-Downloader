from fastapi import APIRouter, HTTPException, status
from schemas import DownloadRequest
from services import download_video, get_metadata
import os

# Define a router for handling the routes
router = APIRouter()

@router.post("/download/")
async def download_video_or_audio(request: DownloadRequest):
    url = request.url
    format = request.format.lower()  # Ensure format is lowercase
    quality = request.quality.lower()  # Ensure quality is lowercase

    # Validate format input
    if format not in ['mp4', 'mkv', 'mp3', 'webm']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid format. Supported formats: mp4, mkv, mp3, 'webm'")

    # Validate quality input for video formats
    valid_qualities = ['360p', '480p', '720p', '1080p', '4k']
    if format in ['mp4', 'mkv', 'webm'] and quality not in valid_qualities:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid quality. Supported qualities: 360p, 480p, 720p, 1080p, 4k")

    try:
        # Call the download_video function to handle the downloading
        file_path = download_video(url, format, quality)

        # Return a success message indicating download started
        return {"status": "success", "message": "Download started", "file_name": os.path.basename(file_path)}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error downloading video: {str(e)}")

@router.get('/metadata')
async def get_metadata_route(url: str):
    metadata = get_metadata(url)
    return metadata
