# services/orc/app/modules/github.py
import logging

# `plans/` used to be populated by cloning github.com/the-peon-project/peon.git and
# sparse-checking-out warplans/ into this path at container startup. Since the
# consolidation into one monorepo, config/docker-compose/02_orc.yml bind-mounts the
# repo's own warplans/ directory here directly (read-only) -- the plans are always
# already current on disk, so there is nothing left to fetch. These functions keep
# their original names/return shape because PUT /api/v1/plans (api_v1.py) and its
# webui/bot-discord callers still expect a {"status": ...} result.

def get_plans_from_github():
    logging.debug("[get_plans_from_github] No-op: plans are served from a read-only bind mount.")
    return {"status": "success"}


def update_plans_from_github(force=False):
    logging.debug("[update_plans_from_github] No-op: plans are served from a read-only bind mount.")
    return {"status": "success"}
