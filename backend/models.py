from datetime import date
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field

class RecurringService(SQLModel, table=True):
    __tablename__ = "recurring_services"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)                 # e.g., "Lift Maintenance", "Generator Service"
    vendor_name: Optional[str] = None
    estimated_amount: Decimal
    frequency_months: int = Field(default=1)      # 1 = Monthly, 3 = Quarterly, 12 = Annual
    last_serviced_date: Optional[date] = None
    next_due_date: date = Field(index=True)
    reminder_days_before: int = Field(default=7)  # Days before due date to alert
    is_active: bool = Field(default=True)

class ServiceLog(SQLModel, table=True):
    __tablename__ = "service_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="recurring_services.id", index=True)
    paid_date: date = Field(default_factory=date.today)
    actual_amount: Decimal
    notes: Optional[str] = None