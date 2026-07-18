import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.book import router as book_router


app = FastAPI()

app.include_router(book_router)    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)