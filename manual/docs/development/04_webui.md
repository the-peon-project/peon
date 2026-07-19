# Web UI

The Web UI module is a supplemental service to the PEON project.

This is a user frontend (website) for managing PEON War Camps.

> **EARLY DEVELOPMENT**
*- Completely useless at this point*

---

## Design Objectives

- Extremely lightweight.
- Aesthetic design principles
- Controls remote systems through REST

---

## Software Stack Diagram

*\*This may change as technologies & skills evolve.*

![Software Stack](../images/diagrams/diagram_webui.png)

---

## Dev Notes

WebUI uses a split architecture:

- Backend API: FastAPI
- Frontend: React (CRACO)
- Runtime packaging: Python backend + nginx static frontend in one container image

For API documentation:

- WebUI backend docs are available at `http://<webui-host>/docs`.
- Selected orchestrator Swagger docs are available through the WebUI proxy at `/api/proxy/{orchestrator_id}/docs`.
- When opened from the dashboard, selected orchestrator Swagger links include the current JWT in the query string so the new tab can authenticate without weakening route security.

This proxy-based docs path replaces the old standalone swagger-ui container in default deployments.

Theme controls are admin-only and live in the Admin panel.

Theme modes:

- `default`: flat slate and light-blue UI with minimal gradients.
- `horde`: a classic warcamp look with iron, bone, leather, and battle-green accents.
- `alliance`: a human castle look with stone, steel, royal blue, and gold accents.

Server detail reads now open inside dedicated dashboard modals instead of expanding additional inline detail blocks on the server management page.

Future UI elements should follow the shared brand rules in the WebUI README before introducing new styling patterns.

Game logos are now served through a backend resolver at `/game-logos/<game_uid>.<ext>`.
When a plan list is fetched or a server is deployed from a recipe, WebUI will automatically hydrate and cache missing logos (including formats like `logo.webp` from `peon-warplans`).

---

## Navigation

Links to various project-related resources.

[![github](../images/buttons/button_github.svg)](https://github.com/the-peon-project/peon-webui)
[![github](../images/buttons/button_bug.svg)](https://github.com/the-peon-project/peon-webui/issues/new/choose)
[![github](../images/buttons/button_changelog.svg)](../development/04_webui.md#release-notes)
[![github](../images/buttons/button_docker.svg)](https://hub.docker.com/repository/docker/umlatt/peon.webui/general)

---

## Features

- [x] Admin user lifecycle controls (create, update, reset password, delete non-self users)
- [x] Server lifecycle controls from dashboard (start, stop, restart, update, delete)

---

## Docker Test Seed Mode

For containerized API test runs, WebUI can seed expected admin users at startup.

Environment variables:

- `PEON_ENABLE_TEST_SEED=true`
- `PEON_TEST_ADMIN_USERNAME` (default: `admin`)
- `PEON_TEST_ADMIN_PASSWORD` (default: `admin123456`)
- `PEON_TEST_DASH_USERNAME` (default: `testadmin`)
- `PEON_TEST_DASH_PASSWORD` (default: `Test1234!`)

This mode is intended for local Docker testing only, for example deployments under `/home/richard/peon`.

When enabled, startup ensures both admin users exist and updates their password/role to the configured values.

When WebUI and ORC are deployed in the same Docker stack, configure the orchestrator in WebUI as `http://peon.orc:5000` so backend API requests resolve through Docker service networking.

---

## Roadmap

- [ ] Recipes - Autodetect newly added recipes.
- [ ] Persistent server data - Keep server data for updates & future releases.
- [ ] WebUI - Access controlled webpage for management
- [ ] Deploy and delete games from a recipe catalog (hosted here)
- [ ] Start/stop servers with timeouts (e.g. specify a game session to run for 6 hours (with the option to extend))

---

## Release Notes

**0.1.10**

- Fixed shared WebUI modal backdrops so server console and related dialogs open as viewport overlays instead of rendering inline below the server list.
- Fixed WebUI server action proxy calls so start, stop, restart, update, and delete requests use the resolved orchestrator URL candidates and the correct delete API semantics.
- Moved GET-driven live server stats into the info modal to keep the main server management grid compact.
- Renamed the `clean` theme to `default`, with legacy browser-stored preferences still migrating automatically.
- Corrected dark-mode heading contrast and aligned Horde and Alliance light-mode surfaces with the default theme's background switching.

**0.1.9**

- Added backend-driven game logo resolution and caching for `/game-logos/*` requests.
- Added automatic logo hydration on recipe plan reads and server deployment actions.
- Fixed missing logos for recipes that only provide non-png assets (for example `palworld/logo.webp`).

**0.1.8**

- Added WebUI controls to delete server instances directly from the server management views.
- Updated user management to allow deleting any account except the currently logged-in user.

**0.1.7**

- Orchestrator URL handling now supports retrying resolved URL candidates for Docker connectivity edge cases.
- WebUI proxy and background sync flows now use the same URL candidate behavior to reduce false timeouts.
- Docker image nginx listener now binds both IPv4 and IPv6 on port 80.
- Deployment guidance now recommends using `http://peon.orc:5000` for local ORC entries in Docker deployments.

**0.1.6**

- [x] Favicon

**0.1.5**

- [x] Logging - Added devMode switch

**0.1.4**

- [x] Dev Tools - Added dev tools to the container
- [x] MOTD - Added motd on login

**0.1.3**

- [x] Base Image Update - Base images were pulled to get the latest versions & app was rebuilt on those

**0.1.2**

- [x] Cleaned up the theme

**0.1.1**

- [x] Initial implementation of python web framework
