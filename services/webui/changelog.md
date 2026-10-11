# PEON UI - Changelog

## 0.2.1

- Friend-group multi-tenancy (Task 1): database schema migration.
  - New tables: `friend_groups`, `group_members`, `group_servers`, `group_announcements`, `admin_alerts`.
  - `chat_messages` gains a `group_id` column (migrated in-place, idempotent).
  - One-time migration guarded by `system_config` key `migration_v3_done`: wipes `chat_messages` and downgrades `moderator` roles to `user` (per approved friend-group design).
  - `get_db()` now resolves `DATABASE_PATH` per connection (container-safe, test-friendly).
  - Test harness: pytest fixtures + 8 schema/migration tests.

## 0.2.0

- Base: Python 3.11 → 3.14 (`python:3.14-slim`, trixie) — latest stable.
- Dependencies: trimmed the backend requirements from a 123-entry freeze to the 11 direct deps the code actually imports (dropped unused tooling, LLM client SDKs, boto3, numpy/pandas/pillow, etc.); transitive deps now resolve fresh at build time. All MIT/Apache-2.0/BSD.
- Frontend build stage unchanged (`node:20-alpine`).

## 0.1.12

- Base Image Update: Runtime stage moved off EOL `python:3.11-slim-bullseye` to `python:3.11-slim` (Debian trixie). Dropped the obsolete `snapshot.debian.org` apt pin in favour of the image's native trixie sources. Frontend build stage unchanged (`node:20-alpine`); app code unchanged.

## 0.1.10-dev

- Modal behavior: Fixed shared dialog backdrops so server console and other overlays render over the viewport instead of inline in page flow.
- Server actions: Fixed proxy execution for start, stop, restart, update, and delete so control requests retry resolved orchestrator URLs and map delete to the orchestrator's supported destroy API.
- Server details: Moved GET-driven runtime stats out of the server grid and into the server info modal for a cleaner server management layout.
- Theme naming: Renamed the `clean` theme to `default` while preserving backward compatibility for stored browser preferences.
- Theme contrast: Corrected dark-mode heading contrast and aligned Horde and Alliance light-mode surfaces with the default theme's background-switching behavior.

## 0.1.7-dev

- Orchestrator connectivity: Added URL candidate resolution with retry support for Docker networking edge cases.
- Proxy resilience: Updated orchestrator connection tests, live server fetches, and background sync to retry alternate resolved URLs.
- Docker runtime: Updated container nginx listener to bind both IPv4 and IPv6 on port 80.
- Docs: Expanded orchestrator URL guidance for standalone Docker deployments and clarified internal service URL usage.

## 0.1.6-dev

- Favicon

## 0.1.5-dev

- Logging - Added devMode switch

## 0.1.4-dev

- Dev Tools - Added dev tools to container
- MOTD - Added motd on login

## 0.1.3-dev

- Base Image Update - Base images were repulled to get latest versions & app rebuilt on those

## 0.1.2-dev

- Cleaned up theme

## 0.1.1-dev

- Initial implementation of flask-python framework
