from database import Base, SessionLocal, engine
from models import MaterialCategory, Recycler, RecyclerRate

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(MaterialCategory).count() > 0:
    print("Already seeded. Nothing to do.")
    raise SystemExit

# --- Material categories (hazard level decides how we guide the collector) ---
categories = [
    (
        "CRT monitor / TV",
        "high",
        "Old tube TVs and monitors. Contain lead glass. Never break or open.",
    ),
    ("LCD / LED panel", "medium", "Flat screens. Handle carefully, do not crush."),
    (
        "Circuit boards (PCB)",
        "medium",
        "Green boards from computers, phones, TVs. Do not burn or acid-wash.",
    ),
    ("Cables and wires", "low", "Copper cables. Do not burn the plastic coating."),
    ("Batteries", "high", "Phone, laptop, inverter batteries. Fire risk if damaged."),
    (
        "Motors and magnet parts",
        "low",
        "Fans, small motors, speakers, hard-disk magnets.",
    ),
    ("Mixed plastics", "low", "Casings and plastic parts from electronics."),
]
cat = {}
for name, hazard, desc in categories:
    c = MaterialCategory(name=name, hazard_level=hazard, description=desc)
    db.add(c)
    cat[name] = c

# --- SAMPLE recyclers (fictional, for development only) ---
recyclers = [
    dict(
        name="SAMPLE Green Cycle Pune",
        address="Hadapsar, Pune",
        lat=18.5089,
        lng=73.9260,
        authorization_number="SAMPLE-0001",
        authorization_status="verified",
        phone="0000000001",
        pickup_available=True,
        service_radius_km=25,
    ),
    dict(
        name="SAMPLE EcoRecover Pimpri",
        address="Pimpri-Chinchwad",
        lat=18.6298,
        lng=73.7997,
        authorization_number="SAMPLE-0002",
        authorization_status="verified",
        phone="0000000002",
        pickup_available=False,
        service_radius_km=15,
    ),
    dict(
        name="SAMPLE NewCycle Bhiwandi",
        address="Bhiwandi, Thane",
        lat=19.3002,
        lng=73.0588,
        authorization_number="SAMPLE-0003",
        authorization_status="pending",
        phone="0000000003",
        pickup_available=True,
        service_radius_km=30,
    ),
]
rec = {}
for r in recyclers:
    obj = Recycler(**r)
    db.add(obj)
    rec[r["name"]] = obj

db.flush()  # gives every row its id

# --- SAMPLE rates in rupees per kg (placeholders, replace after field research) ---
# Note: the second recycler does not accept CRTs. Useful for matching later.
rates = {
    "SAMPLE Green Cycle Pune": {
        "CRT monitor / TV": 3,
        "LCD / LED panel": 8,
        "Circuit boards (PCB)": 180,
        "Cables and wires": 65,
        "Batteries": 30,
        "Motors and magnet parts": 45,
        "Mixed plastics": 8,
    },
    "SAMPLE EcoRecover Pimpri": {
        "LCD / LED panel": 7,
        "Circuit boards (PCB)": 200,
        "Cables and wires": 70,
        "Motors and magnet parts": 42,
        "Mixed plastics": 9,
    },
    "SAMPLE NewCycle Bhiwandi": {
        "CRT monitor / TV": 4,
        "Circuit boards (PCB)": 160,
        "Cables and wires": 60,
    },
}
for rec_name, items in rates.items():
    for cat_name, rate in items.items():
        db.add(
            RecyclerRate(
                recycler_id=rec[rec_name].id,
                category_id=cat[cat_name].id,
                rate_per_kg=rate,
            )
        )

db.commit()
print("Seeded 7 categories, 3 sample recyclers and their rates.")
