# PEON Docs Guide

This repo is the source of truth for PEON documentation. Generated output should not be edited directly unless the task explicitly requires rebuilt artifacts.

## Scope

- Source docs: `manual/docs/`
- Site navigation/config: `manual/zensical.toml`
- Diagram definitions: `diagram_definitions/`
- Build/publish script: `package_docs.sh`
- Generated local site output: `manual/site/`

## Working Rules

1. Edit source files under `manual/docs/`.
2. Treat `manual/site/` as generated output.
3. Treat `../the-peon-project.github.io/` as published/generated output.
4. If code behavior changes elsewhere in the workspace, update the corresponding source docs here.
5. Rebuild generated docs only when the task explicitly includes generated output or publishing.

## Commands

### Source edit workflow

```bash
cd /home/richard/development/peon-docs
```

### Rebuild generated site

```bash
cd /home/richard/development/peon-docs
./package_docs.sh
```

`package_docs.sh` builds the site and copies output into `../the-peon-project.github.io/`.

## Important Files

- Site config and nav: `manual/zensical.toml`
- Top-level docs index: `manual/docs/index.md`
- Developer docs index: `manual/docs/development/index.md`
- API docs: `manual/docs/api/`
- Guides: `manual/docs/guides/`
- Games docs: `manual/docs/guides/games/` and `manual/docs/development/games/`
- Diagram sources: `diagram_definitions/`
- Publish script: `package_docs.sh`

## Validation Expectations

- Validate source edits for correctness and path consistency first.
- Rebuild only when the task needs generated output refreshed.
- If generated output is rebuilt, mention that `the-peon-project.github.io/` was intentionally updated as a consequence.

## Cross-Repo Dependencies

- Reflects behavior across `peon/`, `peon-orc/`, `peon-cli/`, `peon-warplans/`, `peon-wartable/`, `peon-webui/`, and `peon-bot-discord/`
- Game additions or API changes usually require corresponding source-doc updates here

## Default Workflow

1. Find the source docs page that owns the behavior.
2. Update source markdown and navigation if needed.
3. Avoid generated outputs unless explicitly requested.
4. If asked, rebuild with `./package_docs.sh`.
5. Summarize whether the task changed only source docs or also generated site artifacts.