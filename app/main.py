import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Static & template dirs
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/customers", response_class=HTMLResponse)
def read_customers(request: Request, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@app.post("/customers")
def add_customer(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    age: int = Form(None),
    address: str = Form(None),
    phone_number: str = Form(None),
    db: Session = Depends(get_db),
):
    new_customer = models.Customer(
        name=name,
        email=email,
        age=age,
        address=address,
        phone_number=phone_number
    )
    db.add(new_customer)
    db.commit()
    return RedirectResponse(url="/customers", status_code=303)
