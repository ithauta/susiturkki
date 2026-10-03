from tests.conftest import PASSWORD, at, make_app


def test_interface_is_served_for_pages(tmp_path, monkeypatch) -> None:
    _write_ui(tmp_path)
    monkeypatch.setenv("UI_DIR", str(tmp_path))
    app = make_app(at(2025, 10, 15))
    assert app.client.get("/admin").text == "susiturkki"
    assert app.client.get("/assets/app.js").text == "app"
    assert app.client.get("/api/p/missing").status_code == 404


def test_https_cookie_is_marked_secure() -> None:
    app = make_app(at(2025, 10, 15), session_https=True)
    response = app.client.post("/api/admin/login", json={"password": PASSWORD})
    assert "secure" in response.headers["set-cookie"].lower()


def _write_ui(root) -> None:
    (root / "index.html").write_text("susiturkki")
    assets = root / "assets"
    assets.mkdir()
    (assets / "app.js").write_text("app")
