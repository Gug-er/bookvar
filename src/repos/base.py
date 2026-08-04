from sqlalchemy import insert, select, update, delete
from pydantic import BaseModel

from src.db_engine import async_session_maker


class BaseRepository:
    model = None
    schema: BaseModel = None
    
    
    def __init__(self, session):
        self.session = session


    async def get_all(self, limit: int, offset: int) -> list[BaseModel]:
        query = select(self.model)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        
        return [self.schema.model_validate(model) 
                for model in result.scalars().all()]
    
    
    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model:
            return self.schema.model_validate(model)
        else:
            return None
        
        
    async def add(self, data: BaseModel) -> BaseModel:
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return self.schema.model_validate(model)
    
    
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        query = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(query)
        
        
    async def delete_filtered(self, **kwargs) -> BaseModel:
        query = delete(self.model).filter_by(**kwargs).returning(self.model)
        model = await self.session.execute(query)
        return self.schema.model_validate(model)
        