from pydantic import BaseModel

# Pydantic models for request validation
class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"  # Default format is 'mp4'
    quality: str = "720p"  # Default quality is '720p'

class MetadataRequest(BaseModel):
    url: str
