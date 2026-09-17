import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.modules.user import (
    PersistentServerButton,
    USER_PANEL_BUTTON_SPECS,
    USER_PANEL_HANDLERS,
    build_persistent_user_panel,
)


def test_every_button_has_a_handler():
    assert set(USER_PANEL_BUTTON_SPECS) == set(USER_PANEL_HANDLERS)


def test_panel_is_persistent_with_all_actions():
    view = build_persistent_user_panel("ark", "myserver")
    assert view.timeout is None  # required for discord.py to treat it as persistent
    assert len(view.children) == len(USER_PANEL_BUTTON_SPECS)
    actions = {item.action for item in view.children}
    assert actions == set(USER_PANEL_BUTTON_SPECS)


def test_panel_custom_ids_round_trip_through_the_template():
    view = build_persistent_user_panel("ark", "myserver")
    for item in view.children:
        match = PersistentServerButton.__discord_ui_compiled_template__.match(item.custom_id)
        assert match is not None, f"custom_id {item.custom_id!r} does not match the registered template"
        assert match["gameuid"] == "ark"
        assert match["servername"] == "myserver"
        assert match["action"] == item.action


def test_disabled_panel_disables_every_button():
    view = build_persistent_user_panel("ark", "myserver", disabled=True)
    assert all(item.item.disabled for item in view.children)


def test_from_custom_id_reconstructs_the_button_after_a_restart():
    """This is the exact path discord.py takes when an interaction arrives for a button
    with no live Python object in memory -- e.g. right after the bot restarts."""
    import asyncio
    import discord

    match = PersistentServerButton.__discord_ui_compiled_template__.match(
        "peon:userpanel:delete_server:ark:myserver"
    )
    fake_dispatched_item = discord.ui.Button(custom_id="peon:userpanel:delete_server:ark:myserver", label="x")

    reconstructed = asyncio.run(PersistentServerButton.from_custom_id(None, fake_dispatched_item, match))

    assert reconstructed.gameuid == "ark"
    assert reconstructed.servername == "myserver"
    assert reconstructed.action == "delete_server"
