from fastapi import Request

from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.domain.errors import RuleError
from susiturkki.infrastructure.settings import Settings


def get_repository(request: Request) -> SkiRepository:
    return request.app.state.repository


def get_clock(request: Request) -> Clock:
    return request.app.state.clock


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def require_admin(request: Request) -> None:
    if not request.session.get("is_admin"):
        raise RuleError("not_authenticated")
