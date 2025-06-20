from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    email: str
    age: int | None = None
    address: str | None = None
    phone_number: str | None = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True  # or orm_mode = True if you're on Pydantic v1
