from unittest.mock import MagicMock


def test_get_server_requires_auth(client):
    response = client.get("/api/v1/server/info/ark.warcamp1")
    assert response.status_code == 401


def test_get_server_returns_server_info(client, auth_headers, fake_docker_client, monkeypatch):
    from modules import api_v1
    fake_container = MagicMock()
    fake_docker_client.containers.get.return_value = fake_container
    monkeypatch.setattr(api_v1, "server_get_server", lambda container: {"game_uid": "ark", "servername": "warcamp1", "state": "running"})
    response = client.get("/api/v1/server/info/ark.warcamp1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"game_uid": "ark", "servername": "warcamp1", "state": "running"}


def test_get_server_404s_when_container_missing(client, auth_headers, fake_docker_client):
    fake_docker_client.containers.get.side_effect = Exception("not found")
    response = client.get("/api/v1/server/info/ark.missing", headers={"X-Api-Key": "Zu88Zu88"})
    assert response.status_code == 404


def test_put_server_start_requires_warcamp_name_when_not_creating(client, auth_headers):
    response = client.put("/api/v1/server/start/ark", headers=auth_headers, json={})
    assert response.status_code == 400
    assert "warcamp name is required" in response.json()["detail"]["info"]


def test_put_server_unsupported_action_returns_404(client, auth_headers, monkeypatch):
    from modules import api_v1
    monkeypatch.setattr(api_v1, "scheduler_stop_request", lambda server_uid, args: {"response": "later"})
    response = client.put("/api/v1/server/wibble/ark.warcamp1", headers=auth_headers, json={})
    assert response.status_code == 404


def test_delete_server_rejects_unknown_action(client, auth_headers):
    # httpx >= 0.28 dropped the `json`/`data`/`content` kwargs from the
    # `.delete()` convenience method (DELETE-with-body is non-standard);
    # `.request("DELETE", ...)` still supports it.
    response = client.request("DELETE", "/api/v1/server/wibble/ark.warcamp1", headers=auth_headers, json={})
    assert response.status_code == 404
