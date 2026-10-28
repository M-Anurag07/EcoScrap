from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    hazard_level: str
    description: str | None = None


class RecyclerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    authorization_status: str
    phone: str | None = None
    pickup_available: bool
    service_radius_km: float


class PriceBoardItem(BaseModel):
    category_id: int
    category: str
    min_rate: float
    max_rate: float
    avg_rate: float
    recyclers: int
