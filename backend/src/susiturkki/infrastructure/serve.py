import os
import sys
from pathlib import Path


def main() -> None:
    args = uvicorn_args()
    os.execvp(args[0], args)


def uvicorn_args() -> list[str]:
    _ensure_tls_pair()
    return [_uvicorn(), "susiturkki.api.main:app", *_bind(), *_proxy(), *_tls()]


def _uvicorn() -> str:
    sibling = Path(sys.executable).with_name("uvicorn")
    if sibling.is_file():
        return str(sibling)
    return "uvicorn"


def _bind() -> list[str]:
    return ["--host", _required("LISTEN_HOST"), "--port", _required("LISTEN_PORT")]


def _proxy() -> list[str]:
    allowed = os.environ.get("FORWARDED_ALLOW_IPS", "")
    if not allowed:
        return []
    return ["--proxy-headers", "--forwarded-allow-ips", allowed]


def _tls() -> list[str]:
    cert, key = _tls_files()
    if not cert:
        return []
    return ["--ssl-certfile", cert, "--ssl-keyfile", key]


def _ensure_tls_pair() -> None:
    cert, key = _tls_files()
    if bool(cert) != bool(key):
        raise SystemExit("ssl files must be set together")


def _tls_files() -> tuple[str, str]:
    return os.environ.get("SSL_CERT_FILE", ""), os.environ.get("SSL_KEY_FILE", "")


def _required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise SystemExit(f"missing {name}")
    return value


if __name__ == "__main__":
    main()
