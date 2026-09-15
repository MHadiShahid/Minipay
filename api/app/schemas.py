from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    customer_ref: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)


class PaymentCreate(BaseModel):
    transaction_ref: str = Field(min_length=1, max_length=100)
    customer_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)


class CustomerResponse(BaseModel):
    id: int
    customer_ref: str
    name: str
    created_at: str


class PaymentResponse(BaseModel):
    id: int
    transaction_ref: str
    customer_id: int
    amount: Decimal
    status: str
    created_at: str
    completed_at: Optional[str]
    failure_code: Optional[str]