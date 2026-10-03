import pytest

from susiturkki.infrastructure.settings import load_settings


def test_database_path_is_required(monkeypatch) -> None:
    _secrets(monkeypatch)
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    with pytest.raises(RuntimeError, match="missing DATABASE_PATH"):
        load_settings()


def test_session_https_is_required(monkeypatch) -> None:
    _secrets(monkeypatch)
    monkeypatch.delenv("SESSION_HTTPS", raising=False)
    with pytest.raises(RuntimeError, match="missing SESSION_HTTPS"):
        load_settings()


def test_session_https_rejects_other_values(monkeypatch) -> None:
    _secrets(monkeypatch)
    monkeypatch.setenv("SESSION_HTTPS", "yes")
    with pytest.raises(RuntimeError, match="invalid SESSION_HTTPS"):
        load_settings()


def test_session_https_accepts_true(monkeypatch) -> None:
    _secrets(monkeypatch)
    monkeypatch.setenv("SESSION_HTTPS", "true")
    assert load_settings().session_https is True


def _secrets(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_PASSWORD", "secret")
    monkeypatch.setenv("SESSION_SECRET", "session")
    monkeypatch.setenv("DATABASE_PATH", "/data/susiturkki.db")
