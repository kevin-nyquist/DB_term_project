from fastapi import FastAPI

from models import models
from models.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
