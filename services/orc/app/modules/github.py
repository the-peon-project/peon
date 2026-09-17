import logging
from git import Repo
import os
import sys
sys.path.insert(0,'/app')
from modules.shell import execute_shell

plan_path = '/home/peon/plans'
repo_url = 'https://github.com/the-peon-project/peon.git'
# Warplans now live at this subdirectory of the consolidated peon repo (previously
# a standalone peon-warplans repo). We sparse-checkout just this subdir so plan_path
# keeps the flat layout consumers expect (plan_path/plans.json, plan_path/<game_uid>/plan.json).
repo_subdir = 'warplans'

def _flatten_repo_subdir():
    # Copy the sparse-checked-out subdir's contents up to plan_path root, matching
    # the flat layout the old standalone peon-warplans clone used to produce there,
    # then remove the now-redundant nested copy. Safe to delete: a subsequent
    # refresh's `git reset --hard` (see update_plans_from_github) restores it from
    # the sparse-checkout before this function copies it up again.
    execute_shell(cmd_as_string=f'cp -r {plan_path}/{repo_subdir}/. {plan_path}/ && rm -rf {plan_path}/{repo_subdir}')

def get_plans_from_github():
    logging.debug(f'[get_plans_from_github] Pulling latest plans from [{repo_url}] (subdirectory: {repo_subdir}).')
    try:
        execute_shell(cmd_as_string=f'git clone --no-checkout --filter=blob:none {repo_url} {plan_path}')
        execute_shell(cmd_as_string=f'cd {plan_path} && git sparse-checkout init --cone && git sparse-checkout set {repo_subdir} && git checkout main')
        _flatten_repo_subdir()
        return { "status" : "success" }
    except Exception as e:
        logging.error(f'[get_plans_from_github] Could not pull plans from [{repo_url}]. {e}')
        return { "status" : "error", "info" : f"{e}" }

def update_plans_from_github(force=False):
    if not os.listdir(plan_path): # Check if the plans currently exist
        logging.warning(f"[update_plans_from_github] No plans found. Downloading plans from [{repo_url}]")
        if "success" not in (result := get_plans_from_github())['status']: return result
    else: { "status" : "success" }
    try:
        logging.debug(f"[update_plans_from_github] Refreshing the plans from [{repo_url}]")
        # CORRECT SOLUTION [BROKEN]
        #repo = Repo(plan_path)
        #repo.remotes.origin.pull()
        # TEMP SOLUTION [START] - as python git is full of sh**
        execute_shell(cmd_as_string=f'git config --global --add safe.directory {plan_path}')
        if force:
            execute_shell(cmd_as_string=f'cd {plan_path} && git reset --hard && git pull')
        else:
            execute_shell(cmd_as_string=f'cd {plan_path} && git pull')
        # TEMP SOLUTION [END] - as python git is full of sh**
        _flatten_repo_subdir()
        return { "status" : "success" }
    except Exception as e:
        logging.error(f'[get_plans_from_github] Could not pull plans from [{repo_url}]. {e}')
        return { "status" : "error", "info" : f"{e}" }

if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/peon/DEV.peon.orc_github.log', filemode='a', format='%(asctime)s %(thread)d [%(levelname)s] - %(message)s', level=logging.DEBUG)
    update_plans_from_github()
