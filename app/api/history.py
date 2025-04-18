from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List
from app.db.models import DownloadHistory, DownloadHistoryResponse
from app.db.session import get_session

router = APIRouter()

@router.get("/history", response_model=List[DownloadHistoryResponse])
async def get_download_history(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(DownloadHistory))
    return result.all()
