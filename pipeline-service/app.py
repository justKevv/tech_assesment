from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal, Base, get_db
from models.customer import Customer
from services.ingestion import ingest_customers

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    
@app.post("/api/ingest")
def ingest(db = Depends(get_db)):
    records = ingest_customers(db)
    return {"status": "success", "records_processed": records}

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db = Depends(get_db)):
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()
    
    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }    
    
@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db = Depends(get_db)):
    customer = db.query(Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"data": customer}