from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator


def _kilometers(value: object) -> Decimal:
    return Decimal(str(value))


def _optional_kilometers(value: object) -> Decimal | None:
    if value is None or value == "":
        return None
    return Decimal(str(value))


class PasswordBody(BaseModel):
    password: str


class NameBody(BaseModel):
    name: str


class MemberBody(BaseModel):
    given_name: str | None = None
    family_name: str | None = None
    person_id: int | None = None


class PersonNameBody(BaseModel):
    given_name: str
    family_name: str = ""


class EntryBody(BaseModel):
    performed_at: datetime
    distance_km: Annotated[Decimal, BeforeValidator(_kilometers)]
    place: str | None = None
    style: str | None = None
    conditions: str | None = None


class ProfileBody(BaseModel):
    birth_year: int | None = None
    distance_km: Annotated[Decimal | None, BeforeValidator(_optional_kilometers)] = None
    target_on: date | None = None


class AdminEntryBody(EntryBody):
    participant_id: int
