import models  # noqa: F401
from database import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoScrap API")


@app.get("/")
def home():
    return {"message": "EcoScrap backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
