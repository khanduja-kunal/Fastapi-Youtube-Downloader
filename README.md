# Video and Audio Downloader API

This is a **FastAPI** based web application that allows users to download videos and audio from platforms like **YouTube**. The API supports various formats (MP4, MKV, MP3, WebM) and qualities (360p, 480p, 720p, 1080p, 4K). Additionally, the API can fetch metadata for videos without downloading them.

---

## Features

- **Download Videos and Audio**: Users can download videos and audio in different formats like `mp4`, `mkv`, `mp3`, and `webm`.
- **Quality Selection**: Users can specify the quality of videos (`360p`, `480p`, `720p`, `1080p`, `4k`).
- **Metadata Fetching**: Users can get metadata for a video, such as title, duration, views, etc.
- **Automatic Fallback**: If a download fails using `yt-dlp`, the system will fall back to `pytube` for the download.
- **Retry Logic**: The application retries downloading up to 3 times if there’s an error with the download process.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/khanduja-kunal/Fastapi-Youtube-Downloader.git
   cd Fastapi-Youtube-Downloader
   ```

2. **Install the required dependencies**:

   You can use **`pip`** to install the necessary dependencies from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the API**:

   Use **Uvicorn** to run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

2. **Available Endpoints**:

   ### `POST /download/`

   This endpoint allows users to download videos or audio.

   **Request Body**:
   ```json
   {
     "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
     "format": "mp4",   // Default is "mp4"
     "quality": "720p"   // Default is "720p"
   }
   ```

   **Response**:
   ```json
   {
     "status": "success",
     "message": "Download started",
     "file_name": "file_1632948372.mp4"
   }
   ```

   If the download fails, an error response will be returned.

   ### `GET /metadata`

   This endpoint allows users to fetch metadata for a given video URL.

   **Query Parameters**:
   - `url` (required): The URL of the video (e.g., YouTube video URL).

   **Response**:
   ```json
   {
     "title": "Video Title",
     "duration": "120",
     "channel": "Channel Name",
     "thumbnail": "https://link/to/thumbnail.jpg",
     "published_date": "2022-01-01",
     "views": 123456,
     "likes": 1000
   }
   ```

---

## Example Requests

### Download Video Example (using `curl`):
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/download/' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "mp4",
  "quality": "1080p"
}'
```

### Fetch Metadata Example (using `curl`):
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/metadata?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'
```

---

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **yt-dlp**: A powerful command-line tool for downloading videos from YouTube and other sites.
- **pytube**: A lightweight Python library for downloading YouTube content.
- **uvicorn**: ASGI server for running FastAPI apps.

---

## Directory Structure

```
video-audio-downloader-api/
│
├── main.py                  # FastAPI application (routes and logic)
├── routes.py                # Implementation of Routes
├── schemas.py               # Pydantic models for request body
├── services.py              # Core functionality for APIs
├── utils.py                 # Utility function for downloads directory
├── requirements.txt         # Python dependencies
├── downloads/               # Directory where downloaded files will be saved
└── README.md                # Project documentation (this file)
```

---

## Contributing

Feel free to fork this project, make changes, and create a pull request with your improvements!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

---

This is the full content for your `README.md` file. It explains the purpose of the project, installation instructions, how to use it, and gives details about the available endpoints.
