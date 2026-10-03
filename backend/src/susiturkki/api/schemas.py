from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator


def _kilometers(value: object) -> Decimal:
    return Decimal(str(value))


class PasswordBody(BaseModel):
    password: str


class NameBody(BaseModel):
    name: str


class EntryBody(BaseModel):
    performed_at: datetime
    distance_km: Annotated[Decimal, BeforeValidator(_kilometers)]
    place: str | None = None


class AdminEntryBody(EntryBody):
    participant_id: int
