from sqlalchemy import Column, Integer, String
from .database import Base  # make sure Base is imported from your database.py

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)              # added length
    email = Column(String(100), unique=True, index=True) # added length
    age = Column(Integer, nullable=True)
    address = Column(String(200), nullable=True)         # added length
    phone_number = Column(String(20), nullable=True)     # added length
