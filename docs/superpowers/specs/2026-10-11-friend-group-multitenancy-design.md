# Friend-Group Multi-Tenancy — Design

Date: 2026-10-11
Status: **PROPOSED** (awaiting owner approval) — v2 after owner Q&A
Owner: Richard · Builder: PEON

## Intent & Why

Today the PEON Web UI is a single global tenancy: one `users` table with global
roles, one global chat, and server visibility that's either global or relies on
manually-granted per-server links. We want **friend groups** — small private
communities, each with its own **group-admins** and **players**, its own chat,
and its own visible slice of servers — while the **orchestrator fleet stays
shared and platform-admin-managed**.

Success looks like:
- A player logs in and sees only the servers of the groups they belong to, and
  can watch those servers' consoles read-only.
- A group-admin creates a server in their group, picks any fleet orchestrator
  to deploy onto, manages group members, and can promote a specific user to
  **moderator** of a specific server.
- The platform admin (Richard) sees and manages all groups, all members, all
  servers, the whole fleet, and gets alerted to any servers orphaned by a
  deleted group.
- Chat happens inside groups; a global channel carries **platform-admin
  announcements only**.

## The Role Model (agreed with owner, v2)

Four roles, two scopes (group-level vs per-server):

| Role | Scope | Powers |
|---|---|---|
| **platform admin** | global | Everything: all groups, all rosters, all servers across the fleet, fleet (orchestrator) CRUD/activate, global announcements. |
| **group-admin** | per group (the group(s) they're a group-admin in) | Manage that group's roster (add members, set group-admin/player, remove, promote a user to server-moderator), create + manage all servers in the group, deploy into the group on any *active* fleet orchestrator, post in group chat, clear group chat. Bounded to their groups. |
| **moderator** | per server | Manage **one specific server** (start/stop/restart/delete/config/console) that a group-admin or platform admin linked them to. Not group-wide. |
| **player** | per group | **View status + read-only console + game info** for their group's servers. No start/stop, no delete, no config, no backups. Post in group chat. |

Notes:
- A user can belong to **multiple** friend groups, with a different group role
  in each (group-admin in one, player in another).
- "Moderator" is **not** a membership role — it's a per-server grant. It reuses
  the existing `server_links` table: a `manage`-permission link **is** a
  moderator link. (The legacy global `moderator` role in `users.role` is retired.)
- **Platform admin** always passes every check, on every group/server.

## Non-Goals / Anti-Goals

- **No orchestrator self-service.** Orchestrators are the fleet: platform-admin
  CRUD/activate only. Group-admins *select* an orchestrator at deploy; never
  manage one.
- **No billing, quotas, or per-group limits** in this pass.
- **No per-group orchestrator restrictions** (any group can deploy on any
  active fleet orchestrator).
- **No group creation by group-admins** — group creation is platform-admin-only
  (owner: "the admin can manage everything; mods manage groups they're tagged in").

## Data Model (additive; SQLite `/data/peon.db`)

```sql
CREATE TABLE friend_groups (
    id          TEXT PRIMARY KEY,
    name        TEXT UNIQUE NOT NULL,
    description TEXT,
    created_by  TEXT NOT NULL REFERENCES users(id),
    created_at  TEXT NOT NULL
);

CREATE TABLE group_members (
    id            TEXT PRIMARY KEY,
    group_id      TEXT NOT NULL REFERENCES friend_groups(id) ON DELETE CASCADE,
    user_id       TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role          TEXT NOT NULL DEFAULT 'player',   -- 'group-admin' | 'player'
    joined_at     TEXT NOT NULL,
    UNIQUE(group_id, user_id)
);

-- server → group ownership. Absence of a row = "unassigned".
CREATE TABLE group_servers (
    id               TEXT PRIMARY KEY,
    group_id         TEXT NOT NULL REFERENCES friend_groups(id) ON DELETE CASCADE,
    orchestrator_id  TEXT NOT NULL,
    server_uid       TEXT NOT NULL,          -- "<game_uid>.<servername>"
    created_by       TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    UNIQUE(orchestrator_id, server_uid)      -- a server belongs to ≤1 group
);

-- global (group_id NULL) = platform-admin announcements only.
CREATE TABLE group_announcements (
    id          TEXT PRIMARY KEY,
    group_id    TEXT,                          -- NULL = global
    user_id     TEXT NOT NULL REFERENCES users(id),
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

-- pending alerts surfaced to platform admin on next login (e.g. orphaned
-- servers after a group deletion).
CREATE TABLE admin_alerts (
    id              TEXT PRIMARY KEY,
    kind            TEXT NOT NULL,             -- e.g. 'group_deleted_servers'
    message         TEXT NOT NULL,
    detail          TEXT,                      -- JSON, e.g. {"server_uids":[...],"group":"..."}
    created_at      TEXT NOT NULL,
    acknowledged_at TEXT
);
```

- `chat_messages` gains `group_id TEXT` (NULL = global). Existing rows → NULL.
  (SQLite: table-recreate migration, done idempotently at startup.)
- **`server_links`** (existing) is the moderator mechanism: `permissions`
  `'manage'` = moderator-of-that-server, `'read'` = ad-hoc read. Unchanged
  schema; a group-admin (not just platform admin) can now grant it within
  their group.
- **`users.role`**: stays `admin` (platform admin) or `user`. The legacy
  `moderator` value is migrated to `user` in a one-time, logged, reversible
  step (behind a `migrate_roles_v2` system_config flag) — their old global
  chat-moderation power is subsumed by group-admin / server links; platform
  admin (Richard) retains full control.
- `user_orchestrator_access`: retained as a supplementary platform-admin grant;
  not user-facing for group-admins (they always see the active fleet for
  deploy).

## Authorization Matrix (per server S on orchestrator O)

Effective permission = the **maximum** of every grant that applies:

| Grant | Result on S |
|---|---|
| user is platform admin | **manage** (everything) |
| user is group-admin of G and S ∈ G | **manage** |
| `server_link(user, O, S, 'manage')` (moderator) | **manage** |
| user is player of G and S ∈ G | **view + read-only console** |
| `server_link(user, O, S, 'read')` | **view + read-only console** |
| none of the above | **no access** (404 on read, 403 on action) |

- S "belongs to G" = a `group_servers(G, O, S)` row exists. **No row =
  unassigned** → only platform admin and explicit `server_link` holders can
  see it; no group members can.
- **Players** can: get status/stats, read the **console** (read-only stream),
  read game info. They **cannot**: stop/start/restart, delete, change config,
  create backups, or manage access.
- **Deploy** requires `group_id` in the payload for non-admins; the caller must
  be group-admin of that group; the server must not already belong to another
  group. Platform admin's `group_id` is optional (deploy with no group →
  unassigned).
- **Orchestrator list**: platform admin sees all; group-admin sees all *active*
  ones (the deploy picker); players/moderators see none they don't need.

## Group Lifecycle Behaviours (owner decisions, v2)

- **Group deletion — platform admin only** (a group-admin cannot delete a
  group, to prevent a mod nuking a shared group):
  1. Its `group_servers` rows are removed → those servers become **unassigned**
     (kept, **not** deleted).
  2. Each now-unassigned server is **shut down** (stopped, not deleted).
  3. An `admin_alerts` row is written ("N servers from group X are now
     unassigned & stopped") → the platform admin sees a **toast on next login**
     and can acknowledge it.
- **Migration (groups introduced):** every existing server starts
  **unassigned** (no `group_servers` rows) → platform-admin-only until Richard
  assigns each to a group. Existing servers are **left running** at migration
  (no stop — that would be disruptive); only explicit *group deletion* stops
  servers.
  - **Seed data (owner-specified):** create the group **"Jubby land"** and add
    user **jubby** as its **group-admin**.
  - **Chat:** the owner confirmed nothing important is in chat history →
    **wipe all `chat_messages`** at migration (not archived). The `group_id`
    column is still added to the (now empty) table for the new group-chat model.
    This resolves builder call #6 (delete, not archive).

## Backend Changes (services/webui/backend)

1. **`core/security.py`** — add:
   - `user_group_roles(user_id)` → `{group_id: role}`.
   - `server_group(orch_id, server_uid)` → group_id or None.
   - `effective_server_permission(user, orch_id, server_uid)` → 'manage' |
     'view' | None (implements the matrix; platform admin → 'manage').
   - `require_group_admin(current_user, group_id)`, `require_group_member(...)`.
   - Existing `get_current_user` / `get_current_admin_user` unchanged.
2. **New `routes/groups.py`** (`/api/groups`):
   - `GET /` — groups the user is a member of (platform admin: all).
   - `POST /` — create group (**platform admin only**).
   - `GET/PUT/DELETE /{id}` — platform admin only.
   - `GET /{id}/members`, `POST /{id}/members` (add as group-admin|player),
     `PUT /{id}/members/{user_id}` (change role), `DELETE /{id}/members/{user_id}`
     — platform admin always; **group-admin of own group** allowed; guard:
     can't remove/demote the last group-admin unless platform admin.
   - `GET /{id}/orchestrators` — active fleet orchestrators (deploy picker).
3. **`routes/proxy.py`**:
   - `get_servers`: replace current `server_links`-only filter with the full
     matrix (group servers ∪ server_links; admin unfiltered).
   - `deploy_server`: enforce `group_id` (non-admin) + group-admin check + no
     double-group; record `group_servers` row.
   - `server_action` + `proxy_orchestrator` catch-all: gate on
     `effective_server_permission` (view-only console path for players; manage
     actions for group-admin/moderator/platform admin).
   - `grant_server_access` / `get_server_access_users`: allow group-admin of
     the owning group (not just platform admin) to create a moderator (`manage`)
     link within their group.
4. **`routes/chat.py`** — messages carry `group_id`; reads limited to the
   user's groups + global; writes: group posts need membership, global posts
   need platform admin; `/clear` becomes per-group (group-admin clears own
   group; admin any + global).
5. **`routes/admin.py`** — user management shows group memberships; existing
   link endpoints remain.
6. **`routes/system.py`** — new `GET /api/system/pending-alerts`
   (unacknowledged `admin_alerts`) + `POST /api/system/pending-alerts/{id}/ack`;
   the frontend toasts on login.
7. **Migration** in `core/database.py` (idempotent, startup): create tables,
   recreate `chat_messages` with `group_id`, one-time logged `moderator`→`user`
   role flip behind `migrate_roles_v2` flag, seed no `group_servers` (existing
   = unassigned). **Tested against a copy of the live DB before rollout.**

## Frontend Changes (services/webui/frontend)

- **Role model surfaced** as platform admin / group-admin / moderator / player.
- **Group context** in the top bar: current group picker (drives servers +
  chat); "All my groups" option for the server grid.
- **Groups page** (platform admin): create/edit/delete groups, roster
  management, group-admin/player toggle.
- **Group-admin roster view**: add members, set roles, **link a user as
  moderator to a specific server**, clear group chat.
- **Deploy flow**: group-admin picks their group + active orchestrator, then
  the plan form.
- **Servers grid**: group badge; **players** see a read-only console (no
  stop/start/delete buttons, no config tab, no backups).
- **Chat**: per-group tabs + a read-only **Announcements** tab (platform admin
  posts; everyone reads).
- **Login toast**: pending `admin_alerts` (e.g. orphaned servers) shown to the
  platform admin.
- Existing React+CRACO stack + `api.js`; **no new frontend deps**.

## Constraints & Compliance

- Python 3.14 / FastAPI; **no new third-party deps** (SQLite + stdlib + existing)
  → license framework unaffected.
- Additive, idempotent schema migration; existing DB preserved (tested on a copy).
- Orchestrator API keys never exposed by group endpoints.
- Rollout: webui image **0.3.0** (minor — new tenancy model); build, verify
  against DB copy + a throwaway group flow, then deploy with the
  recreate-with-alias discipline (restore `webapp` alias) used on the 3.14
  rollout.

## Builder's Calls (settled; flag any you disagree with)

1. **Group creation & group deletion = platform-admin only.** Group-admins
   manage roster + servers, not the group's existence (prevents a mod from
   deleting a shared group).
2. **Moderator = `server_link(…, 'manage')`.** Reuses the existing per-server
   grant table; no new "moderators" table. Group-admins can grant it within
   their group; platform admin anywhere.
3. **Player console is read-only** (live tail), no process control — per your
   answer.
4. **Deploy requires `group_id` for non-admins**; rejected if the caller isn't
   group-admin of it or the server is already grouped. A group-admin with no
   groups simply can't deploy (they get one when admin creates the group).
5. **Migration leaves existing servers running** (only explicit group *deletion*
   stops servers) to avoid a disruptive mass-stop at rollout.
6. **Legacy global chat** (rows with no group) is treated as the global
   channel = admin-announce-only going forward; prior public messages remain
   stored but the channel's rules change. (If you want old chat preserved as a
   distinct readable archive instead, say so — it's a small change.)
7. **Global = `group_id IS NULL`** in both `chat_messages` and
   `group_announcements`; only platform admin writes there.
