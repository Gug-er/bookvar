import uvicorn
from fastapi import FastAPI

from src.api.admin import router as admin_router
from src.api.auth import router as auth_router
from src.api.user import router as user_router
from src.api.book import router as book_router

app = FastAPI()

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(book_router)    


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)