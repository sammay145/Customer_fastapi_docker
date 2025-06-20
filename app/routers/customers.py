from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER

from .. import crud, schemas
from ..database import SessionLocal
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/customers", response_class=HTMLResponse)
def read_customers(request: Request, db: Session = Depends(get_db)):
    customers = crud.get_customers(db)
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@router.post("/customers", response_class=HTMLResponse)
def create_customer(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    customer = schemas.CustomerCreate(name=name, email=email)
    crud.create_customer(db, customer)
    return RedirectResponse(url="/customers", status_code=HTTP_303_SEE_OTHER)
