import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


def install_ui(app: FastAPI) -> None:
    root = _ui_root()
    if root is not None:
        app.add_api_route("/{full_path:path}", _reader(root), methods=["GET"], include_in_schema=False)


def _ui_root() -> Path | None:
    raw = os.environ.get("UI_DIR", "")
    root = Path(raw) if raw else None
    if root is not None and root.is_dir():
        return root
    return None


def _reader(root: Path):
    def read_page(full_path: str) -> FileResponse:
        return _file_for(root, full_path)

    return read_page


def _file_for(root: Path, full_path: str) -> FileResponse:
    if full_path.startswith("api"):
        raise HTTPException(status_code=404)
    return _existing(root, full_path)


def _existing(root: Path, full_path: str) -> FileResponse:
    candidate = (root / full_path).resolve()
    if _inside(root, candidate):
        return FileResponse(candidate)
    return FileResponse(root / "index.html")


def _inside(root: Path, candidate: Path) -> bool:
    return candidate.is_file() and candidate.is_relative_to(root.resolve())
