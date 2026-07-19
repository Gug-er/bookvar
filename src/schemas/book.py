from pydantic import BaseModel, ConfigDict

class BookAdd(BaseModel):
    title: str
    author: str
    year: int
    annotation: str
    genre: str

class BookSchema(BookAdd):
    id: int
    
    
    model_config = ConfigDict(
        from_attributes=True
    )