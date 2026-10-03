from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from susiturkki.api.admin import public, secured
from susiturkki.api.errors import register_errors
from susiturkki.api.participant import router
from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.infrastructure.clock import SystemClock
from susiturkki.infrastructure.settings import Settings
from susiturkki.infrastructure.sqlite import SqliteSkiRepository


def create_app(settings: Settings, repository: SkiRepository | None = None, clock: Clock | None = None) -> FastAPI:
    app = FastAPI(title="Susiturkki")
    _attach_state(app, settings, repository, clock)
    _install(app, settings)
    return app


def _attach_state(app: FastAPI, settings: Settings, repository: SkiRepository | None, clock: Clock | None) -> None:
    app.state.settings = settings
    app.state.repository = repository or SqliteSkiRepository(settings.database_path)
    app.state.clock = clock or SystemClock()


def _install(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, same_site="lax", https_only=False)
    register_errors(app)
    app.include_router(router)
    app.include_router(public)
    app.include_router(secured)
