import asyncio

from src.utils.db_manager import DBManager
from src.database import async_session_maker


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db
        

DBDep = Annotated[DBManager, Depends(get_db)]