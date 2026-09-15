# PEON Docs Guide

This directory is the source of truth for PEON documentation. Formerly the standalone `peon-docs` repo, now `peon/docs/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map). Generated output should not be edited directly unless the task explicitly requires rebuilt artifacts.

Read this file first at the start of work in this directory. Keep changes minimal and directory-local unless the task is explicitly cross-directory, and use non-destructive validation first.

## Scope

- Source docs: `manual/docs/`
- Site navigation/config: `manual/zensical.toml`
- Diagram definitions: `diagram_definitions/`
- Build/publish script: `package_docs.sh`
- Generated local site output: `manual/site/`

## Working Rules

1. Edit source files under `manual/docs/`.
2. Treat `manual/site/` as generated output — do not hand-edit it.
3. Treat `/home/richard/development/the-peon-project.github.io/` as published/generated output — do not hand-edit it. This is a **separate, standalone repo at the workspace root**, a sibling of `peon/` itself, not of `peon/docs/`. It was deliberately left out of the monorepo consolidation and keeps its own history.
4. If code behavior changes elsewhere in the `peon` monorepo, update the corresponding source docs here in the same pass.
5. Rebuild generated docs only when the task explicitly includes generated output or publishing.

## Commands

### Source edit workflow

```bash
cd /home/richard/development/peon/docs
```

### Rebuild generated site

```bash
cd /home/richard/development/peon/docs
./package_docs.sh
```

`package_docs.sh` builds the site and copies output to the absolute, hardcoded path `/home/richard/development/the-peon-project.github.io/`. That path is independent of where this directory lives in the workspace, so the script itself needed no changes when `peon-docs` moved into `peon/docs/` — only this guide's prose did.

## Important Files

- Site config and nav: `manual/zensical.toml`
- Top-level docs index: `manual/docs/index.md`
- Developer docs index: `manual/docs/development/index.md`
- API docs: `manual/docs/api/` (also see `api/` at this directory's root)
- Guides: `manual/docs/guides/`
- Games docs: `manual/docs/guides/games/` and `manual/docs/development/games/`
- Diagram sources: `diagram_definitions/`
- Publish script: `package_docs.sh`

## Validation Expectations

- Validate source edits for correctness and path consistency first.
- Rebuild only when the task needs generated output refreshed.
- If generated output is rebuilt, mention that `/home/richard/development/the-peon-project.github.io/` was intentionally updated as a consequence, since it's an external repo outside this monorepo.

## Cross-Directory Dependencies (within this repo)

- This directory documents behavior across all subdirectories of the `peon` monorepo (`services/orc`, `services/webui`, `services/bot-discord`, `cli`, `warplans`, `wartable`, and the root deployment wiring).
- Game additions or API changes elsewhere in the monorepo usually require corresponding source-doc updates here.

## Default Workflow

1. Find the source docs page that owns the behavior.
2. Update source markdown and navigation if needed.
3. Avoid generated outputs unless explicitly requested.
4. If asked, rebuild with `./package_docs.sh`.
5. Summarize whether the task changed only source docs or also the external generated site repo.
