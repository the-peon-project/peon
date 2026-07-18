#!/usr/bin/python3
import json
import logging
import os
import shutil
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from modules import prefix, settings
from .peon import get_warcamp_name
from .servers import *
from .plans import *
from .security import *
from .scheduler import *
router = APIRouter()


def _require_authorized(request: Request) -> None:
    if not authorized(request.headers):
        raise HTTPException(status_code=401, detail="Not authorized")


async def _request_payload(request: Request) -> dict[str, Any]:
    try:
        payload = await request.json()
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return {}


@router.get("/orchestrator")
def get_orchestrator(request: Request):
    logging.info("APIv1 [GET] Orchestrator")
    _require_authorized(request)
    try:
        return {"version": os.environ.get("VERSION", "-.-.-")}
    except Exception as e:
        logging.error(f"Failed to get Orchestrator information. {e}")
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "info": "There was an issue getting the Orchestrator information."},
        )


@router.get("/server/{action}/{server_uid}")
def get_server(action: str, server_uid: str, request: Request):
    logging.info(f"APIv1 [GET] Server <{server_uid}>")
    _require_authorized(request)
    try:
        server = server_get_server(client.containers.get(f"{prefix}{server_uid}"))
        if action == "stats":
            server["stats"] = server_get_stats(server_uid)
        elif action == "save":
            file_path = server_download_files(server_uid)
            return FileResponse(path=file_path, filename=os.path.basename(file_path))
        return server
    except Exception as e:
        logging.error(f"Failed to get server information. {e}")
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "info": "There was an issue getting the server."},
        )


@router.put("/server/{action}/{server_uid}")
async def put_server(action: str, server_uid: str, request: Request):
    logging.info(f"APIv1 [PUT] server <{action}> <{server_uid}>")
    _require_authorized(request)

    args = await _request_payload(request)
    result = {"status": "success"}
    clean_on_fail = False
    server_uid_parts = server_uid.split('.')
    args['game_uid'] = server_uid_parts[0]

    if len(server_uid_parts) < 2:
        if 'create' not in action:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "info": f"For the requested action [{action}] a warcamp name is required. You only provided [{server_uid}]",
                },
            )
        args['warcamp'] = get_warcamp_name()
        server_uid = f"{args['game_uid']}.{args['warcamp']}"
    else:
        args['warcamp'] = server_uid_parts[1]

    args['server_path'] = f"{settings['path']['servers']}/{args['game_uid']}/{args['warcamp']}"

    if action == "create":
        logging.debug("create.01. Check if there are preloaded server files.")
        if not os.path.isdir(args['server_path']):
            clean_on_fail = True
        logging.debug("create.02. Trigger [create_new_warcamp] with with settings.")
        result = create_new_warcamp(config_peon=settings, user_settings=args)
        if 'success' in result['status']:
            if args.get('start_later'):
                logging.info("create.03. Server created successfully. No-start flag set.")
                return {
                    "status": "success",
                    "info": f"The server files for [{args['warcamp']}] were created, but the server was not started, in accordance with the provided settings.",
                }
            logging.debug("create.03. Server created successfully.")
            action = 'start'

    if action == "update":
        mode = args.get('mode', 'full')
        logging.debug("update.01. Running update sequence.")
        result = server_update(server_uid, mode.lower())
        if result['status'] != "success":
            raise HTTPException(status_code=400, detail=result)
        return result

    if action == "start":
        logging.debug("start.01. Check and configure server shutdown time.")
        result = scheduler_stop_request(server_uid, args)
        if "response" not in result:
            raise HTTPException(status_code=400, detail=result)
        logging.debug("start.02. Trigger the startup of the server.")
        result = server_start(server_uid)
    elif action == "stop":
        logging.debug("stop.01. Check if automated shutdown is being requested server shutdown time.")
        result = scheduler_stop_request(server_uid, args)
        if "response" in result and result["response"] == "NOW":
            logging.debug("[stop][02] Triggering server shutdown.")
            scheduler_remove_exisiting_stop(server_uid)
            result = server_stop(server_uid)
    elif action == "restart":
        logging.debug("restart.01. Restarting server.")
        result = server_restart(server_uid)
    elif action == "description":
        try:
            logging.debug("description.01. Updating the server description.")
            result = server_update_description(server_uid=server_uid, description=args["description"])
        except Exception:
            raise HTTPException(
                status_code=400,
                detail={"status": "error", "info": "The description argument was incorrectly provided."},
            )
    elif action == "skip":
        logging.debug("skip.01. Skip additional actions requested.")
    else:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "info": result.get('info', f"Unsupported action [{action}].")},
        )

    time.sleep(0.5)
    if "success" in result["status"]:
        logging.debug("Fetching the status of the server.")
        server = server_get_server(client.containers.get(f"{prefix}{server_uid}"))
        return server

    if clean_on_fail:
        if args.get('noclean'):
            logging.info("Do not clean on failure flag was set.")
        else:
            logging.warning(f"Removing server {server_uid} folder from filesystem.")
            shutil.rmtree(args['server_path'])
    raise HTTPException(status_code=400, detail=result)


@router.delete("/server/{action}/{server_uid}")
async def delete_server(action: str, server_uid: str, request: Request):
    logging.info(f"APIv1 [DEL] server <{action}> <{server_uid}>")
    _require_authorized(request)

    args = await _request_payload(request)
    note = ""
    if action not in ["destroy", "eradicate"]:
        raise HTTPException(status_code=404, detail={"error": f"Incorrect action [{action}] provided"})

    if action == "destroy":
        logging.debug("Removing the server container environment.")
        result = server_delete(server_uid)
        if 'success' not in result['status']:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "info": f"Failed to remove the server [{server_uid}]",
                    "exception": f"{result['exception']}",
                },
            )
        note = f"Server {server_uid} was removed. "

    if args.get("eradicate"):
        logging.debug("Removing the server & user data from the filesystem.")
        server_delete_files(server_uid)
        note = note + f"All files for {server_uid} will be purged from the server. This may take a few moments."
    return {"status": "success", "info": note}


@router.get("/servers")
def get_servers(request: Request):
    logging.info("APIv1 [GET] servers - list all servers")
    _require_authorized(request)
    return servers_get_all()


@router.put("/servers")
def put_servers(request: Request):
    logging.info("APIv1 [PUT] servers - import")
    _require_authorized(request)
    servers_import()
    return servers_get_all()


@router.get("/plans")
def get_plans(request: Request):
    logging.info("APIv1 [GET] plans")
    _require_authorized(request)
    config_peon = json.load(open("/app/config.json", 'r'))
    if plans := get_plans_local(config_peon=config_peon):
        return plans
    raise HTTPException(status_code=404, detail="There was an issue getting the local plans list.")


@router.put("/plans")
def put_plans(request: Request):
    logging.info("APIv1 [PUT] plans <update>")
    _require_authorized(request)

    old_plans = get_plans_local(settings)
    result = update_latest_plans_from_repository()
    if 'success' not in result['status']:
        raise HTTPException(status_code=404, detail=result)

    new_plans = get_plans_local(settings)
    differences = {}
    for new_dict in new_plans:
        game_uid = new_dict['game_uid']
        found = False
        for old_dict in old_plans:
            if old_dict['game_uid'] == game_uid:
                found = True
                break
        if not found:
            differences[game_uid] = new_dict
    configure_plan_permissions()
    return {"new_recipies": differences}


@router.get("/plan/{game_uid}")
def get_plan(game_uid: str, request: Request):
    logging.info(f"APIv1 [GET] plans <{game_uid}>")
    _require_authorized(request)

    config_peon = json.load(open("/app/config.json", 'r'))
    if settings_data := get_all_required_settings(config_peon=config_peon, game_uid=game_uid):
        return settings_data
    raise HTTPException(status_code=404, detail=f"Could not get the settings for [{game_uid}]")
            
