from pydantic import BaseModel, ConfigDict, Field

class BookAdd(BaseModel):
    title: str
    author: str
    year: int
    annotation: str
    genre: str


class BookPatch(BaseModel):
    title: str | None = Field(default=None)
    author: str | None = Field(default=None)
    year: int | None = Field(default=None)
    annotation: str | None = Field(default=None)
    genre: str | None = Field(default=None)


class BookSchema(BookAdd):
    book_id: int
    
    
    model_config = ConfigDict(
        from_attributes=True
    )