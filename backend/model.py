from typing import Optional, Any
import re
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class ServantRoom(BaseModel):
    room_number: str
    area: int
    assigned_to_flat: Optional[str] = None

class Flat(BaseModel):
    flat_number: str
    area: int
    family_name: str
    servant_room: Optional[ServantRoom] = None

    @property
    def total_chargeable_area(self) -> int:
        extra_area = self.servant_room.area if self.servant_room else 0
        return self.area + extra_area

class BillCategory(str, Enum):
    SECURITY = "security"
    ELECTRICITY = "common_electricity"
    WATER = "common_water"

class ResolvedBill(BaseModel):
    category: BillCategory
    amount: Decimal
    source: str

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, value: Any) -> Decimal:
        if isinstance(value, str):
            cleaned = re.sub(r"[^\d.-]]", "", value.strip())
            return Decimal(cleaned)
        return Decimal(str(value))


class BillExtractionSchema(BaseModel):
    category: str = Field(description="One of: security, common_electricity, common_water")
    total_amount: Decimal = Field(description="The total net amount payable as a decimal number")
    due_date: Optional[str] = Field(description="Due date, if present")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0")

    @field_validator("total_amount", mode="before")
    @classmethod
    def clean_decimal_string(cls, value: Any) -> Decimal:
        if isinstance(value, (int, float, Decimal)):
            return Decimal(str(value))

        if isinstance(value, str):
            cleaned = re.sub(r"[^\d.-]]", "", value.strip())
            if not cleaned:
                raise ValueError("No valid numeric digits found in extracted amount")
            return Decimal(cleaned)
        raise ValueError(f"Invalid input type for decimal: {type(value)}")

class FlatShare(BaseModel):
    flat_number: str
    area: int
    share_amount: Decimal