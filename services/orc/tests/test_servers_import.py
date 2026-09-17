from unittest.mock import MagicMock


def test_servers_import_skips_already_registered_server(monkeypatch):
    from modules import servers

    monkeypatch.setattr(
        servers.os, "walk",
        lambda base_path: iter([
            ("/home/peon/servers/ark/existing", [], ["docker-compose.yml"]),
        ]),
    )
    monkeypatch.setattr(servers, "server_check", lambda server_uid: MagicMock())
    execute_shell_mock = MagicMock()
    monkeypatch.setattr(servers, "execute_shell", execute_shell_mock)

    servers.servers_import()

    execute_shell_mock.assert_not_called()


def test_servers_import_creates_unregistered_server(monkeypatch):
    from modules import servers

    monkeypatch.setattr(
        servers.os, "walk",
        lambda base_path: iter([
            ("/home/peon/servers/ark/newserver", [], ["docker-compose.yml"]),
        ]),
    )
    monkeypatch.setattr(servers, "server_check", lambda server_uid: "error")
    execute_shell_mock = MagicMock()
    monkeypatch.setattr(servers, "execute_shell", execute_shell_mock)

    servers.servers_import()

    execute_shell_mock.assert_called_once()
    assert "ark_newserver" in execute_shell_mock.call_args[0][0]


def test_servers_import_continues_after_one_directory_fails(monkeypatch):
    """A CalledProcessError (or any exception) creating one server must not abort the scan."""
    from modules import servers

    monkeypatch.setattr(
        servers.os, "walk",
        lambda base_path: iter([
            ("/home/peon/servers/broken/instance", [], ["docker-compose.yml"]),
            ("/home/peon/servers/ark/newserver", [], ["docker-compose.yml"]),
        ]),
    )
    monkeypatch.setattr(servers, "server_check", lambda server_uid: "error")

    calls = []

    def fake_execute_shell(cmd):
        calls.append(cmd)
        if "broken_instance" in cmd:
            raise Exception("docker compose create failed: container name conflict")
        return []

    monkeypatch.setattr(servers, "execute_shell", fake_execute_shell)

    servers.servers_import()  # must not raise despite the first directory failing

    assert len(calls) == 2
    assert any("ark_newserver" in c for c in calls)
