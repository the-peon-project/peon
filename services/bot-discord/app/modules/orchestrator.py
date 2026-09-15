# IMPORT
import logging
from datetime import datetime
import pytz
import requests
import aiohttp
import re
import json
import os
from . import *

REQUEST_TIMEOUT = 10


def _get_config_path(filename: str) -> str:
    return os.path.join(CONFIG_DIR, filename)


def _request_json(method, url, headers=None, json_body=None, timeout=REQUEST_TIMEOUT):
    """Execute an HTTP request and normalize error handling for callers."""
    try:
        response = requests.request(method, url, headers=headers, json=json_body, timeout=timeout)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as exc:
        logging.error(f"HTTP request failed [{method}] {url}: {exc}")
        return {"status": "error", "message": str(exc)}
    except ValueError as exc:
        logging.error(f"Invalid JSON response [{method}] {url}: {exc}")
        return {"status": "error", "message": "Invalid JSON response"}

# Load orchestrators from disk
def get_peon_orcs():
    try:
        config_file = _get_config_path("peon.orchestrators.json")
        logging.debug("Loading orchestrators file")
        with open(config_file, 'r') as file:
            orchestrators = json.load(file)
        api_key = os.environ.get('LOCAL_API_KEY', None)
        if api_key:
            updated = False
            for entry in orchestrators:
                if entry["url"] == "http://peon.orc:5000":
                    if entry.get("key") != api_key:
                        logging.debug("Updating orchestrator API key")
                        entry["key"] = api_key
                        updated = True
                    break
            if updated:
                with open(config_file, 'w') as file:
                    json.dump(orchestrators, file, indent=4)
        return {"status": "success", "data": orchestrators}
    except FileNotFoundError:
        logging.debug("No orchestrators file found. Creating one.")
        default_data = []
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as file:
            json.dump(default_data, file, indent=4)
        return {"status": "error", "info": "Orchestrators file not found. Created a new one."}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"status": "error", "info": str(e)}

def register_peon_orc(orc_name, orc_url, orc_key):
    try:
        orchestrators = get_peon_orcs()
        if orchestrators["status"] == "error":
            return orchestrators
        orchestrators = orchestrators["data"]
        for entry in orchestrators:
            if entry["name"] == orc_name:
                return {"status": "error", "info": "Orchestrator already registered."}
        if (orc_responose := get_orchestrator_details(orc_url, orc_key))['status'] != "success":
            return {"status": "error", "info": "Orchestrator not available."}
        orchestrators.append({"name": orc_name, "url": orc_url, "key": orc_key})
        config_file = _get_config_path("peon.orchestrators.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as file:
            json.dump(orchestrators, file, indent=4)
        return {"status": "success", "info": orc_responose['data']}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"status": "error", "info": str(e)}

def get_orchestrator_details(url, api_key):
    url = f"{url}/api/v1/orchestrator"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    result = _request_json("GET", url, headers=headers)
    if result["status"] == "success":
        return {"status": "success", "data": result["data"]}
    return result

async def get_orchestrator_details_async(url, api_key):
    """Async version of get_orchestrator_details for use in Discord callbacks"""
    endpoint_url = f"{url}/api/v1/orchestrator"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                response.raise_for_status()
                data = await response.json()
                return { "status" : "success", "data" : data }
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching orchestrator details: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logging.error(f"Unexpected error fetching orchestrator details: {e}")
        return {"status": "error", "message": str(e)}

# Services Get users in a certain group
def deregister_peon_orc(orc_name):
    try:
        orchestrators = get_peon_orcs()
        if orchestrators["status"] == "error":
            return orchestrators
        orchestrators = orchestrators["data"]
        updated_orchestrators = [orc for orc in orchestrators if orc["name"] != orc_name]
        if len(updated_orchestrators) == len(orchestrators):
            return {"status": "error", "info": "Orchestrator not found."}
        config_file = _get_config_path("peon.orchestrators.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as file:
            json.dump(updated_orchestrators, file, indent=4)
        return {"status": "success", "info": f"Orchestrator '{orc_name}' has been deregistered."}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"status": "error", "info": str(e)}

def get_servers(url, api_key):
    url = f"{url}/api/v1/servers"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    result = _request_json("GET", url, headers=headers)
    if result["status"] != "success":
        return []
    if isinstance(result["data"], list):
        return result["data"]
    return []

def import_servers(url, api_key):
    url = f"{url}/api/v1/servers"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    return _request_json("PUT", url, headers=headers)

def get_all_plans(url, api_key):
    url = f"{url}/api/v1/plans"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    return _request_json("GET", url, headers=headers)

def update_plans(url, api_key):
    url = f"{url}/api/v1/plans"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    return _request_json("PUT", url, headers=headers)

def server_create(url, api_key, game_uid, warcamp_name, user_settings=None):
    if user_settings is None:
        user_settings = {}
    server_uid = f"{game_uid}.{warcamp_name}"
    endpoint_url = f"{url}/api/v1/server/create/{server_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    body = {"game_uid": game_uid, "warcamp": warcamp_name, **user_settings}
    
    # Log the request details for debugging
    logging.info(f"Creating server: {server_uid}")
    logging.info(f"Request URL: {endpoint_url}")
    logging.info(f"Request headers: {headers}")
    logging.info(f"Request body: {body}")
    
    result = _request_json("PUT", endpoint_url, headers=headers, json_body=body)
    if result["status"] == "success":
        return result
    logging.error(f"Error creating server: {result.get('message', 'Unknown error')}")
    return result

def test_orchestrator_connectivity(url, api_key):
    """Test connectivity to orchestrator and list available plans"""
    try:
        # Test basic connectivity
        orchestrator_url = f"{url}/api/v1/orchestrator"
        headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
        response = requests.get(orchestrator_url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        logging.info(f"Orchestrator connectivity OK: {response.json()}")
        
        # Get available plans
        plans_url = f"{url}/api/v1/plans"
        plans_response = requests.get(plans_url, headers=headers, timeout=REQUEST_TIMEOUT)
        plans_response.raise_for_status()
        
        plans = plans_response.json()
        logging.info(f"Available plans: {plans}")
        
        return {
            "status": "success",
            "orchestrator_info": response.json(),
            "available_plans": plans
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Error testing orchestrator connectivity: {e}")
        return {"status": "error", "message": str(e)}

def server_delete(url, api_key, server_uid, action="destroy", eradicate=False):
    url = f"{url}/api/v1/server/{action}/{server_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    body = {"eradicate": eradicate} if eradicate else {}
    return _request_json("DELETE", url, headers=headers, json_body=body)

def server_get_save_download(url, api_key, server_uid):
    url = f"{url}/api/v1/server/save/{server_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    result = _request_json("GET", url, headers=headers)
    if result["status"] == "success":
        return {"status": "success", "download_url": url}
    return result

def server_update_description(url, api_key, server_uid, description):
    url = f"{url}/api/v1/server/description/{server_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    body = {"description": description}
    return _request_json("PUT", url, headers=headers, json_body=body)

def get_servers_all(peon_orchestrators):
    response=""
    for orchestrator in peon_orchestrators:
        response += f"The warcamp/s on {orchestrator['name'].upper()} are in the current state/s\n```yaml"
        for server in get_servers(orchestrator['url'], orchestrator['key']):
            server_uid = f"{server['game_uid']}.{server['servername']}"
            response += "\n{0:<25} : {1}".format(server_uid,server['container_state'])
        response += "\n```"
    return { "status" : "success", "data" : f"{response}" }

def import_warcamps(peon_orchestrators):
    logging.debug('Requesting import of unmanaged warcamps')
    warcamps={}
    for orchestrator in peon_orchestrators:
        url = f"{orchestrator['url']}/api/v1/servers"
        headers = { 'Accept': 'application/json', 'X-Api-Key': orchestrator['key'] }  
        response = requests.put(url, headers=headers)
        if response.status_code != 200:
            warcamps[orchestrator['name']] = {}
        else:
            warcamps[orchestrator['name']] = response.json()
    if not warcamps: return { "status" : "error", "err_code" : "orc.notavailable", "command" : "import"}
    reponse_warcamps = {}
    for orc, servers in warcamps.items():
        response_string = f"Orc {orc.upper()} now has the following warcamps.\n```yaml"
        for server in servers:
            response_string += "\n{0:<15} : {1}".format(server['game_uid'],server['servername'])
        response_string += "\n```"
        reponse_warcamps[orc] = response_string
    return { "status" : "success", "data" : reponse_warcamps }

def refresh_warplans(peon_orchestrators):
    logging.debug('Requesting an update to plans catalogue')
    url = f"{peon_orchestrators[0]['url']}/api/v1/plans"
    headers = { 'Accept': 'application/json', 'X-Api-Key': peon_orchestrators[0]['key'] }
    response = requests.put(url, headers=headers, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        return { "status" : "error", "err_code" : "plan.update", "command" : "refresh"}
    else:
        return { "status" : "success"}
    
def get_warplans(peon_orchestrators):
    logging.debug('Requesting list of current plans')
    url = f"{peon_orchestrators[0]['url']}/api/v1/plans"
    headers = { 'Accept': 'application/json', 'X-Api-Key': peon_orchestrators[0]['key'] }
    plans = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT).json()
    response = f"*The currently available warplans for your ochestrators.*\n```yaml"
    response += "\n{0:<15} : {1}\n{2:<15} : {2}".format("game_uid","game","---")
    for plan in plans:
        response += "\n{0:<15} : {1}".format(plan['game_uid'],plan['title'])
    response += "\n```"
    return { "status" : "success", "data" : f"{response}" }

def get_warplan(peon_orchestrators,game_uid):
    logging.debug('Requesting details for the warplan related to {game_uid}')
    url = f"{peon_orchestrators[0]['url']}/api/v1/plan/{game_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': peon_orchestrators[0]['key'] }
    plan = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    if plan.status_code != 200:
        return { "status" : "error", "err_code" : "plan.dne", "command" : "plan"}
    response = f"*Warplan takes the following settings.*\n```json"
    for key, value in plan.json().items():
        response += "\n{0:<15} : {1}".format(key,value)
    response += "\n```"
    return { "status" : "success", "data" : f"{response}" }

def server_backup(url, api_key, server_uid):
    logging.debug(f'[serverBackup] - {server_uid}]')
    url = f"{url}/api/v1/server/save/{server_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    return (requests.put(url, headers=headers, timeout=REQUEST_TIMEOUT)).json()

def server_action(url, api_key, server_uid, action, body=None):
    if body is None:
        body = {}
    logging.debug(f'[server_action] - {action} requested for {server_uid}: body {body}')
    url = f"{url}/api/v1/server/{action}/{server_uid}"
    headers = { 'Accept': 'application/json', 'X-Api-Key': api_key }
    if action == "get":
        return (requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)).json()
    return (requests.put(url, headers=headers, json=body, timeout=REQUEST_TIMEOUT)).json()

def server_actions(action,args):
    logging.debug(f"Server action requested: {action}")
    logging.debug("STEP 1 - Check for active orchestrators")
    if len(args) == 0: return { "status" : "error", "err_code" : "srv.param", "command" : action}
    # STEP 1: Check that there are some registered orchestrators
    if 'error' in (result := get_peon_orcs())['status']: return { "status" : "error", "err_code" : "orc.none", "command" : action}
    peon_orchestrators = result['data']
    if action != 'get':
        #STEP 2: Get argument information
        logging.debug("STEP 2 - Check for arguments")
        arg_datetime = look_for_regex_in_args(r"^(\d{4})\W(\d{2})\W(\d{2})\.(\d{2})[:h](\d{2})$",args)
        if arg_datetime: args.remove(arg_datetime)
        arg_time = look_for_regex_in_args(r"^(\d{2})[:h](\d{2})$",args)
        if arg_time: args.remove(arg_time)
        arg_interval = look_for_regex_in_args(r"^\d+.?$",args) # Look for a string of type D..DC (e.g. 5m, 20h, 3d)
        time_unit=""
        if not arg_interval:
            if (arg_interval := look_for_regex_in_args(r"^\d+$",args)): time_unit = 'm' # If several digits are provided then assume it is a minute count
        if arg_interval: 
            args.remove(arg_interval)
            arg_interval += time_unit
        arg_update_mode = look_for_regex_in_args("^(server|image|full|reinit)$", args)
        if arg_update_mode:
            args.remove(arg_update_mode)
        if len(args) < 1: return { "status" : "error", "err_code" : "srv.param", "command" : action}
    else: logging.debug("No arguments required for 'get' action. Skipping to STEP 3.")
    # STEP 3: Get list of servers on orchestrators
    logging.debug("STEP 3 - Collect all servers on all orchestrators")
    ## SCALE ISSUE: If there are lots of Orcs, it could take time (so, if people end up using this, rewrite). Then we need a local DB
    server_list = []
    server = {}
    for orchestrator in peon_orchestrators:
        try:
            servers = get_servers(orchestrator['url'], orchestrator['key'])
            for server in servers:
                server['orchestrator'] = orchestrator['name']
            server_list.extend(servers)
        except:
            logging.warning(f"Host {orchestrator} is unavailable.")
    if len(server_list) == 0: return { "status" : "error", "err_code" : "orc.notavailable", "command" : action}
    # STEP 4: Try and find server with remaining arg/s
    logging.debug("STEP 4 - Filter by 'servername'")
    servers_matching_servername = []
    for server in server_list:
        arg_servername = look_for_regex_in_args(server['servername'].lower(),args)
        if arg_servername:
            servers_matching_servername.append(server)
    server_list = servers_matching_servername
    if len(server_list) == 0: 
        logging.error('Server not found')
        return { "status" : "error", "err_code" : "srv.dne", "command" : action}
    elif len(server_list) > 1:
        logging.debug("STEP 5 - Filter by 'game_uid'")
        servers_matching_gameuid = []
        for server in server_list:
            arg_gameuid = look_for_regex_in_args(server['game_uid'].lower(),args)
            if arg_gameuid:
                servers_matching_gameuid.append(server)
        server_list = servers_matching_gameuid
        logging.debug("STEP 6 - Filter by Orchestrator")
        if len(server_list) == 0: return { "status" : "error", "err_code" : "srv.dne", "command" : action}
        elif len(server_list) > 1:
            matched_orchestrator_list = []
            for server in server_list:
                arg_orchestrator = look_for_regex_in_args(server['orchestrator'].lower(),args)
                if arg_orchestrator:
                    matched_orchestrator_list.append(server)
                    break
            server_list = matched_orchestrator_list
            if len(server_list) > 1: return { "status" : "error", "err_code" : "srv.notexplicit", "command" : action}
            else:
                logging.debug("Server found, skipping to STEP 7")
    else:
        logging.debug("Server found, skipping to STEP 7")
    server = server_list[0]
    if server['servername'] in args:
        args.remove(server['servername'])
    if server['game_uid'] in args: args.remove(server['game_uid'])
    logging.debug(f"STEP 7 - Trigger [{action}] action on server")
    serveruid=f"{server['game_uid']}.{server['servername']}"
    orchestrator = next((orc for orc in peon_orchestrators if orc['name'] == server['orchestrator']), None)
    if orchestrator is None:
        return {"status": "error", "err_code": "orc.notavailable", "command": action}
    data = server_action(orchestrator['url'],orchestrator['key'],serveruid,'get')
    if "error" in data:
        response = { "status" : "error", "err_code" : "srv.action.error", "command" : action}
    else:
        response = ""
        if action == 'get':
            if "time" not in args:
                response = "```yaml\n{0:<15}: {1}\n{2:<15}: {3}\n{4:<15}: {5}\n{6:<15}: {7}\n{8:<15}: {9}\n".format(
                    "Warcamp",data["servername"],
                    "Type",data['game_uid'],
                    "Peon State",(data["server_state"].lower()),
                    "Server Type",f"{data['container_type']}:{data['build_version']}",
                    "Description",data["description"]
                    )
                try:
                    if data['server_config']:
                        response += "---\n"
                        config_dict = data['server_config']
                        for key,value in config_dict.items():
                            response += "{0:<15}: {1}\n".format(key.title(),value)
                except:
                    response += f"---\n{data['server_config']}\n"
                response += "```"
            if data["time"]: 
                if data["server_state"].lower() == 'running':
                    if data["time"] is not None:
                        today = pytz.utc.localize(datetime.today()).astimezone(pytz.timezone(settings["timezone"]))
                        stoptime = pytz.utc.localize(datetime.fromtimestamp(int(data["time"]))).astimezone(pytz.timezone(settings["timezone"]))
                        response += "\n\t:alarm_clock: Orc will turn off server at ``"
                        if str(today.date()) == str(stoptime.date()): response += stoptime.strftime("%X %Z")
                        else: response += stoptime.strftime("%X %Z [%x]")
                        response += "``"
                    else:
                        response += "\n\t:bell: Server does not have a shutdown schedule."
                else:
                    if "time" in args: response += "\n\t:alarm_clock: Server is not in running state."
        else:
            body = {}
            if arg_time:
                date_string = (datetime.now(pytz.timezone(settings["timezone"])).date().strftime('%Y-%m-%d'))
                timestring = re.match(r"^(\d{2})[:h](\d{2})$",arg_time)
                timestring = f"{date_string} {timestring[1]}:{timestring[2]}:00"
                time_tz = pytz.timezone(settings["timezone"]).localize(datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S'))
                epoch = int(time_tz.timestamp())
                if epoch <= int(datetime.now(pytz.timezone(settings["timezone"])).timestamp()):
                    return { "status" : "error", "err_code" : "schedule.past", "command" : action}
                body = {"epoch_time" : f"{epoch}"}
                response += f"\n\n\t:alarm_clock: Warcamp will shut down at ``{timestring}``."
            elif arg_datetime:
                timestring = re.match(r"^(\d{4})\W(\d{2})\W(\d{2})\.(\d{2})[:h](\d{2})$",arg_datetime)
                timestring = (f"{timestring[1]}-{timestring[2]}-{timestring[3]} {timestring[4]}:{timestring[5]}:00")
                time_tz = pytz.timezone(settings["timezone"]).localize(datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S'))
                epoch = int(time_tz.timestamp())
                if epoch <= int(datetime.now(pytz.timezone(settings["timezone"])).timestamp()):
                    return { "status" : "error", "err_code" : "schedule.past", "command" : action}
                body = {"epoch_time" : f"{epoch}"}
                response += f"\n\n\t:alarm_clock: Warcamp will shut down at ``{timestring}``."
            elif arg_interval:
                body = { "interval" : f"{arg_interval}" }
                response += f"\n\n\t:alarm_clock: Warcamp will shut down in ``{arg_interval}``."
            elif arg_update_mode:
                body = { "mode" : f"{arg_update_mode}" }
                response += f"\n\n\t:arrows_counterclockwise: Warcamp will do a ``{arg_update_mode}`` update."
            # logging.debug("STEP 8 - Permissions check")
            data = server_action(orchestrator['url'], orchestrator['key'], serveruid, action, body)
            if "error" in data:
                return { "status" : "error", "err_code" : "srv.action.error", "command" : action}
            else:
                response += str(data)
        return { "status" : "success", "data" : f"{response}" }
