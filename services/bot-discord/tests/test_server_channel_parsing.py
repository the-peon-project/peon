import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.modules.shared import parse_server_channel_name


def test_parse_server_channel_name_basic():
    assert parse_server_channel_name("minecraft-survival") == ("minecraft", "survival")
    assert parse_server_channel_name("cs2-vanilla-1") == ("cs2", "vanilla-1")
    assert parse_server_channel_name("rust-lobby-west") == ("rust", "lobby-west")


def test_parse_server_channel_name_invalid():
    assert parse_server_channel_name("peon") is None
    assert parse_server_channel_name("single") is None
    assert parse_server_channel_name("") is None
