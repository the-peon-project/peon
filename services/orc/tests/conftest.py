# services/orc/tests/conftest.py
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

APP_DIR = Path(__file__).resolve().parent.parent / "app"
os.environ["PEON_INSTALL_PATH"] = str(APP_DIR)
os.environ.setdefault("API_KEY", "Zu88Zu88")

# `modules/__init__.py` calls docker.from_env() at import time — patch it out
# before anything under app/ is ever imported, so tests never need a real
# Docker daemon.
import docker  # noqa: E402
docker.from_env = MagicMock(name="docker.from_env")

sys.path.insert(0, str(APP_DIR))


@pytest.fixture()
def fake_docker_client():
    """The mocked docker.DockerClient shared by every orc module (modules.client)."""
    from modules import client
    client.reset_mock(return_value=True, side_effect=True)
    return client


@pytest.fixture()
def app(fake_docker_client):
    from fastapi import FastAPI
    from modules.api_v1 import router as api_v1_router
    test_app = FastAPI()
    test_app.include_router(api_v1_router, prefix="/api/v1")
    return test_app


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture()
def auth_headers():
    return {"X-Api-Key": "Zu88Zu88"}
