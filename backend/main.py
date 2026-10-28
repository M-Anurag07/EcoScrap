from database import Base, engine, get_db
from fastapi import Depends, FastAPI
from models import MaterialCategory, Recycler, RecyclerRate
from schemas import CategoryOut, PriceBoardItem, RecyclerOut
from sqlalchemy import func
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoScrap API")


@app.get("/")
def home():
    return {"message": "EcoScrap backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(MaterialCategory).all()


@app.get("/recyclers", response_model=list[RecyclerOut])
def list_recyclers(db: Session = Depends(get_db)):
    # Only verified recyclers are shown to collectors
    return db.query(Recycler).filter(Recycler.authorization_status == "verified").all()


@app.get("/price-board", response_model=list[PriceBoardItem])
def price_board(db: Session = Depends(get_db)):
    rows = (
        db.query(
            MaterialCategory.id,
            MaterialCategory.name,
            func.min(RecyclerRate.rate_per_kg),
            func.max(RecyclerRate.rate_per_kg),
            func.avg(RecyclerRate.rate_per_kg),
            func.count(RecyclerRate.id),
        )
        .join(RecyclerRate, RecyclerRate.category_id == MaterialCategory.id)
        .join(Recycler, Recycler.id == RecyclerRate.recycler_id)
        .filter(Recycler.authorization_status == "verified")
        .group_by(MaterialCategory.id)
        .all()
    )
    return [
        PriceBoardItem(
            category_id=r[0],
            category=r[1],
            min_rate=r[2],
            max_rate=r[3],
            avg_rate=round(r[4], 1),
            recyclers=r[5],
        )
        for r in rows
    ]
