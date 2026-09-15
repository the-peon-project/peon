"""One-off migration: replace the repeated server_start boilerplate with calls
into wartable/containers/_shared/init/lib/server_start_lib.sh. Run once from the
repo root: python3 warplans/tools/migrate_server_start.py [--apply]
Without --apply it only prints which files it would change (dry run)."""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WARPLANS_DIR = REPO_ROOT / "warplans"
SOURCE_LINE = "source /init/lib/server_start_lib.sh"

BANNER_RE = re.compile(r'^echo "###### Server ([^.]+)\.\$SERVER_NAME \[STARTING\]"$', re.MULTILINE)
LD_ENTER_RE = re.compile(
    r"^export templdpath=\$LD_LIBRARY_PATH\nexport LD_LIBRARY_PATH=\./linux64:\$LD_LIBRARY_PATH$",
    re.MULTILINE,
)
LD_EXIT_RE = re.compile(r"^export LD_LIBRARY_PATH=\$templdpath$", re.MULTILINE)


def migrate_one(text: str) -> str | None:
    if not BANNER_RE.search(text) or not LD_ENTER_RE.search(text) or not LD_EXIT_RE.search(text):
        return None  # doesn't match the skeleton — leave untouched (e.g. windrose)

    def banner_sub(m: re.Match) -> str:
        return f'peon_server_starting "{m.group(1)}"'

    new_text = BANNER_RE.sub(banner_sub, text, count=1)
    new_text = LD_ENTER_RE.sub("peon_steam_ld_path_enter", new_text, count=1)
    new_text = LD_EXIT_RE.sub("peon_steam_ld_path_exit", new_text, count=1)

    lines = new_text.splitlines()
    if lines and lines[0] == "#!/bin/bash":
        lines.insert(1, SOURCE_LINE)
    else:
        lines.insert(0, SOURCE_LINE)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main() -> None:
    apply = "--apply" in sys.argv
    changed = []
    for script in sorted(WARPLANS_DIR.glob("*/actions/server_start")):
        original = script.read_text()
        migrated = migrate_one(original)
        if migrated is None or migrated == original:
            continue
        changed.append(script)
        if apply:
            script.write_text(migrated)
    mode = "Migrated" if apply else "Would migrate"
    print(f"{mode} {len(changed)} file(s):")
    for path in changed:
        print(f"  {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
