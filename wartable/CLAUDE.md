# PEON Wartable Guide

This directory owns container image definitions used by PEON game deployments. Formerly the standalone `peon-wartable` repo, now `peon/wartable/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map).

## Scope

- Image build/push script: `build_containers`
- Image definitions: `containers/`
- Current container families: `containers/steamcmd/`, `containers/steamcmd-proton/`, `containers/steamcmd-wine/`, each with a `Dockerfile`, `README.md`, `init/`, `media/`, and `tools/`
- Shared base image: `containers/_base/` — all three variants above now `FROM` this image (see `containers/_base/Dockerfile`) instead of duplicating identical setup steps. `_base/init/` is a real, hand-synced directory (not a symlink) because Docker's `COPY` can't follow a symlink pointing outside its build context.
- Canonical shared source: `containers/_shared/` — holds the files that used to be triplicated across the three variants (`init/*`, `tools/modules/shared`). Each variant's `init/*` and `tools/modules/shared` are symlinks pointing back into `_shared/`. `_shared/init` is itself a symlink to `../_base/init`, so there is exactly one real copy of the init assets (`_base/init/`); everything else — `_shared/init` and all three variants' `init/*` symlinks — transitively resolves to it. Editing `_base/init/*` is the only way to change what actually ships in a built image.

## Working Rules

1. Start from the specific image directory under `containers/`.
2. Treat image names, entrypoints, environment variables, and mounted init assets as contract points for downstream directories. `_base/init/lib/server_start_lib.sh` is one such contract point: `warplans/<game>/actions/server_start` scripts `source` it directly by absolute path (`/init/lib/server_start_lib.sh`), so changing its function names or signatures is a breaking change for every migrated game plan.
3. Review whether plan modes or image names in `peon/warplans` rely on the image being changed.
4. Do not push or overwrite remote images unless the user explicitly asked for that release action. There is no CI/CD for this directory — image publishing is a manual, human-triggered step.
5. If runtime behavior changes, update `peon/docs` source docs.
6. Keep changes minimal and directory-local unless the task is explicitly cross-directory.
7. Use non-destructive validation first; do not request or print secrets; do not edit generated docs outputs directly.

## Commands

Static review is preferred first. Images are pushed manually to Docker Hub (`umlatt/steamcmd`, `umlatt/steamcmd-proton`, `umlatt/steamcmd-winehq`) via the build script:

```bash
cd /home/richard/development/peon/wartable
./build_containers <version> [--overwrite]
```

Treat that as a release-oriented action, not default validation. The docker compose flow is the only sanctioned way to build and ship a feature — never treat a native run or a hand-copied file as shipped. For deployment or release validation, build updated images from source under this directory, then upgrade the UAT/prod stack at `/home/richard/peon/` (a separate deployed instance, distinct from this dev checkout — reachable at `https://server.warcamp.org`) via `peon/deploy_peon.sh` before sign-off.

`build_containers` builds and pushes the shared `umlatt/peon-steamcmd-base` image (from `containers/_base/`) before building the three variants, so the base is always published together with whatever variant versions reference it in the same run — a variant Dockerfile's `ARG BASE_VERSION` build-arg pins it to that exact base version (via `docker build --build-arg BASE_VERSION="$version" ...` in `containers/_shared/tools/modules/shared`'s `build_container_image()`) rather than always floating to whatever `:latest` base image happens to be cached locally on the build host.

## Important Files

- Build/push script: `build_containers`
- Image definitions: `containers/steamcmd/`, `containers/steamcmd-proton/`, `containers/steamcmd-wine/`
- Example image definition: `containers/steamcmd/Dockerfile`

## Validation Expectations

- Prefer static Dockerfile review and narrow image-surface inspection first.
- If executable validation is required, use the smallest local Docker build path that matches the task, and prefer targeted container build checks scoped to the touched image.
- Avoid pushing images unless explicitly requested.

## Cross-Directory Dependencies (within this repo)

- `peon/warplans` references image names and modes that depend on this directory
- `peon/services/orc` relies on compatible image behavior at runtime
- `peon/docs` should reflect meaningful image/runtime behavior changes

## Default Workflow

1. Identify the affected container family.
2. Read the Dockerfile and adjacent init/tools files.
3. Make the smallest packaging change needed.
4. Validate with static review or a narrow Docker check.
5. Update docs if behavior changed.
