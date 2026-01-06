from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status
from typing import Optional


class ExpenseCreate(BaseModel):
    description: str = Field(
        ..., min_length=5, max_length=255, description="describe what it is spent to"
    )
    amount: float = Field(..., gt=0)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("add description")
        return stripped

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v is None:
            raise ValueError("add amount")
        return v


class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float

    model_config = {"from_attributes": True}


class ExpenseUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=4, max_length=255)
    amount: Optional[float] = Field(None, gt=0)

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("توضیح نمی‌تواند خالی یا فقط فضای خالی باشد")
        return v.strip() if v is not None else None
