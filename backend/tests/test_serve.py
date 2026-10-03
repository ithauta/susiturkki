import pytest

from susiturkki.infrastructure.serve import uvicorn_args


def test_forwarded_header_is_optional(monkeypatch) -> None:
    _listen(monkeypatch)
    _clear_tls(monkeypatch)
    monkeypatch.delenv("FORWARDED_ALLOW_IPS", raising=False)
    assert "--proxy-headers" not in uvicorn_args()


def test_proxy_trusts_only_the_given_addresses(monkeypatch) -> None:
    _listen(monkeypatch)
    _clear_tls(monkeypatch)
    monkeypatch.setenv("FORWARDED_ALLOW_IPS", "*")
    args = uvicorn_args()
    assert args[args.index("--forwarded-allow-ips") + 1] == "*"


def test_tls_needs_both_files(monkeypatch) -> None:
    _listen(monkeypatch)
    monkeypatch.setenv("SSL_CERT_FILE", "/cert.pem")
    monkeypatch.delenv("SSL_KEY_FILE", raising=False)
    with pytest.raises(SystemExit):
        uvicorn_args()


def test_tls_flags_follow_the_files(monkeypatch) -> None:
    _listen(monkeypatch)
    monkeypatch.setenv("SSL_CERT_FILE", "/cert.pem")
    monkeypatch.setenv("SSL_KEY_FILE", "/key.pem")
    args = uvicorn_args()
    assert args[args.index("--ssl-certfile") + 1] == "/cert.pem"


def _listen(monkeypatch) -> None:
    monkeypatch.setenv("LISTEN_HOST", "0.0.0.0")
    monkeypatch.setenv("LISTEN_PORT", "9")


def _clear_tls(monkeypatch) -> None:
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.delenv("SSL_KEY_FILE", raising=False)
