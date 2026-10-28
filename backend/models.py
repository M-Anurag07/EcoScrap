from datetime import datetime

from database import Base
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Collector(Base):
    __tablename__ = "collectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    preferred_language: Mapped[str] = mapped_column(String(5), default="hi")
    area: Mapped[str | None] = mapped_column(String(100))
    pin_hash: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MaterialCategory(Base):
    __tablename__ = "material_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    hazard_level: Mapped[str] = mapped_column(String(10), default="low")
    description: Mapped[str | None] = mapped_column(Text)


class Recycler(Base):
    __tablename__ = "recyclers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    address: Mapped[str | None] = mapped_column(Text)
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)
    authorization_number: Mapped[str | None] = mapped_column(String(100))
    authorization_status: Mapped[str] = mapped_column(String(20), default="pending")
    phone: Mapped[str | None] = mapped_column(String(20))
    pickup_available: Mapped[bool] = mapped_column(Boolean, default=False)
    service_radius_km: Mapped[float] = mapped_column(Float, default=20)


class RecyclerRate(Base):
    __tablename__ = "recycler_rates"
    id: Mapped[int] = mapped_column(primary_key=True)
    recycler_id: Mapped[int] = mapped_column(ForeignKey("recyclers.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id"))
    rate_per_kg: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Lot(Base):
    __tablename__ = "lots"
    id: Mapped[int] = mapped_column(primary_key=True)
    lot_ref: Mapped[str] = mapped_column(String(30), unique=True)
    collector_id: Mapped[int] = mapped_column(ForeignKey("collectors.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id"))
    description: Mapped[str | None] = mapped_column(Text)
    image_path: Mapped[str | None] = mapped_column(String(255))
    weight_kg: Mapped[float] = mapped_column(Float)
    condition: Mapped[str | None] = mapped_column(String(30))
    estimated_value: Mapped[float | None] = mapped_column(Float)
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PriceHistory(Base):
    __tablename__ = "price_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id"))
    location: Mapped[str] = mapped_column(String(100))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    buying_price: Mapped[float] = mapped_column(Float)
    quoted_price: Mapped[float | None] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10), default="kg")
    recycler_id: Mapped[int | None] = mapped_column(ForeignKey("recyclers.id"))


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    recycler_id: Mapped[int] = mapped_column(ForeignKey("recyclers.id"))
    quoted_price: Mapped[float] = mapped_column(Float)
    final_price: Mapped[float | None] = mapped_column(Float)
    payment_status: Mapped[str] = mapped_column(String(20), default="pending")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Handover(Base):
    __tablename__ = "handovers"
    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    reference_code: Mapped[str] = mapped_column(String(30), unique=True)
    photo_path: Mapped[str | None] = mapped_column(String(255))
    weight_kg: Mapped[float | None] = mapped_column(Float)
    gps_lat: Mapped[float | None] = mapped_column(Float)
    gps_lng: Mapped[float | None] = mapped_column(Float)
    handed_over_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    recycler_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime)


class EndOfLifeGuidance(Base):
    __tablename__ = "end_of_life_guidance"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id"))
    step_order: Mapped[int] = mapped_column(default=1)
    action_type: Mapped[str] = mapped_column(String(20))
    text_en: Mapped[str] = mapped_column(Text)
    text_hi: Mapped[str | None] = mapped_column(Text)
    text_mr: Mapped[str | None] = mapped_column(Text)
    audio_path: Mapped[str | None] = mapped_column(String(255))
