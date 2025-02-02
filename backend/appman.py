import uvicorn
import logging
from abc import ABC
import subprocess
from sys import exit
from typing import Optional

# from const import HOST, PORT, DB_FILE, RUN_DIR
from const import HOST, PORT, Paths
from utils import buildDirectories, isBinary
from db import Database

# GLOBALS

class AbstractAppMan(ABC):
    def startApp(self, script_name: str, program_name: str):
        logging.debug(f"Start app called for {Paths.RUN_DIR.value + script_name}")
        if not script_name.endswith(".sh") and not isBinary(script_name):
            logging.error(f'script_name format is wrong {script_name} must be a ".py", ".sh" or a binary')
            return
        else:
            isRunning = subprocess.run([f"ps aux | grep {program_name} | grep -v grep"], shell=True, capture_output=True, text=True)
            print(f"IS RUNNING: {isRunning.stdout}")
            if isRunning.stdout == "":
                result = subprocess.run([Paths.RUN_DIR.value + script_name, "-a"], stderr=subprocess.PIPE)
                logging.info(f"Started application: {script_name} succesfully")
            else:
                logging.info(f"Application {script_name} already running so not started")
                # raise Exception(f"{program_name} already running")

class AppMan(AbstractAppMan):
    def __init__(self):
        buildDirectories()
        self.db: Database = Database()
        self.startActiveApps()

    def ApiRequests(self, request: str, arg: Optional[str] = None):
        if request == "list":
            ret = {}
            for name, app in self.db.apps.items():
                ret[name] = app.to_dict()
            return ret
        elif request == "refresh":
            self.db.updateApps()
        elif request == "activate":
            print(f"pre: {arg}")
            self.db.activateApp(arg)
            self.startApp(self.db.apps[arg].run, self.db.apps[arg].program_name)
        elif request == "deactivate":
            self.db.deactivateApp(arg)

    def startActiveApps(self):
        logging.info(f"start active apps called")
        for name, app in self.db.apps.items():
            if app.active:
                try:
                    logging.info(f"Launching: {name}, filename: {app.run}")
                    self.startApp(app.run, app.program_name)
                except Exception as e:
                    logging.error(f"Could not execute subprocess to start app: {e}")
