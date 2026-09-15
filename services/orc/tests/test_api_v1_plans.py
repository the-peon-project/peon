def test_get_plans_requires_auth(client):
    response = client.get("/api/v1/plans")
    assert response.status_code == 401


def test_get_plans_returns_local_plans_sorted_by_title(client, auth_headers, monkeypatch):
    from modules import api_v1
    fake_plans = [
        {"title": "Zeta Game", "game_uid": "zeta"},
        {"title": "Alpha Game", "game_uid": "alpha"},
    ]
    monkeypatch.setattr(api_v1, "get_plans_local", lambda config_peon: sorted(fake_plans, key=lambda p: p["title"]))
    response = client.get("/api/v1/plans", headers=auth_headers)
    assert response.status_code == 200
    titles = [p["title"] for p in response.json()]
    assert titles == ["Alpha Game", "Zeta Game"]


def test_get_plans_404s_when_local_plans_missing(client, auth_headers, monkeypatch):
    from modules import api_v1
    monkeypatch.setattr(api_v1, "get_plans_local", lambda config_peon: None)
    response = client.get("/api/v1/plans", headers=auth_headers)
    assert response.status_code == 404


def test_get_plan_returns_required_settings(client, auth_headers, monkeypatch):
    from modules import api_v1
    monkeypatch.setattr(
        api_v1, "get_all_required_settings",
        lambda config_peon, game_uid: {"SERVER_NAME": "", "description": f"A PEON game server for {game_uid}."},
    )
    response = client.get("/api/v1/plan/ark", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["description"] == "A PEON game server for ark."


def test_get_plan_404s_for_unknown_game(client, auth_headers, monkeypatch):
    from modules import api_v1
    monkeypatch.setattr(api_v1, "get_all_required_settings", lambda config_peon, game_uid: None)
    response = client.get("/api/v1/plan/does-not-exist", headers=auth_headers)
    assert response.status_code == 404
