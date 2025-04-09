import yt_dlp
import os
import time
from pytube import YouTube
from fastapi import HTTPException, status

# Directory to store downloaded files
DOWNLOAD_DIR = 'downloads'

# Function to handle video/audio download and conversion using yt-dlp
def download_video_yt_dlp(url: str, format: str, quality: str):
    timestamp = int(time.time())
    file_extension = format if format != 'mp3' else 'mp3'
    file_name = f"file_{timestamp}.{file_extension}"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best available audio
            'outtmpl': file_path,
        }
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={quality.replace("p", "")}]+bestaudio/best',
            'outtmpl': file_path,
            'merge_output_format': format,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(file_path):
            return file_path
        else:
            raise Exception("Download failed with yt-dlp.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"yt-dlp error: {str(e)}")

# Function to handle video/audio download and conversion using pytube (fallback)
def download_video_pytube(url: str, format: str, quality: str):
    try:
        yt = YouTube(url)
        # Select stream based on quality
        stream = yt.streams.filter(progressive=True, file_extension=format).get_by_resolution(quality)
        if not stream:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No streams found for {quality} quality.")
        
        # Download the video
        timestamp = int(time.time())
        file_name = f"file_{timestamp}.{format if format != 'mp3' else 'mp3'}"
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
        
        stream.download(output_path=DOWNLOAD_DIR, filename=file_name)
        
        return file_path
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"pytube error: {str(e)}")

# Function to manage the download process with retry and fallback
def download_video(url: str, format: str, quality: str):
    attempts = 3
    for attempt in range(attempts):
        try:
            # Try to download using yt-dlp
            return download_video_yt_dlp(url, format, quality)
        except HTTPException as e:
            if attempt < attempts - 1:  # Retry if not the last attempt
                time.sleep(1)  # Wait a little before retrying
            else:
                # After 3 attempts, fall back to pytube
                return download_video_pytube(url, format, quality)

# Function to fetch metadata from YouTube video
def get_metadata(url: str):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=False)

            metadata = {
                'title': data.get('title', 'N/A'),
                'duration': data.get('duration', 'N/A'),
                'channel': data.get('uploader', 'N/A'),
                'thumbnail': data.get('thumbnail', 'N/A'),
                'published_date': data.get('upload_date', 'N/A'),
                'views': data.get('view_count', 'N/A'),
                'likes': data.get('like_count', 'N/A')
            }
            return metadata
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error getting metadata: " + str(e))
