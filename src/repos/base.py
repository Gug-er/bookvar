from sqlalchemy import select
from pydantic import BaseModel

from src.database import async_session_maker


class BaseRepository:
    model = None
    schema: BaseModel = None
    
    
    def __init__(self, session):
        self.session = session
    
    
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        
        return [self.schema.model_validate(model) 
                for model in result.scalars().all()]
    
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model:
            return self.schema.model_validate(model)
        else:
            return None