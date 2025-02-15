import uvicorn
import logging
from abc import ABC
import subprocess
from sys import exit
from typing import Optional

from const import HOST, PORT, Paths
from utils import buildDirectories, isBinary, isRunning
from db import Database

class AbstractAppMan(ABC):
    def startApp(self, script_name: str, program_name: str):
        logging.debug(f"Start app called for {Paths.RUN_DIR.value + script_name}")
        if not script_name.endswith(".sh") and not isBinary(script_name):
            logging.error(f'script_name format is wrong {script_name} must be a ".py", ".sh" or a binary')
            return
        else:
            if not isRunning(program_name=program_name):
                path = Paths.RUN_DIR.value + script_name
                subprocess.Popen([path, "--activate"], close_fds=True, start_new_session=True)
                logging.info(f"Started application: {script_name} succesfully")
            else:
                logging.info(f"Application {script_name} already running so not started")

    def stopApp(self, script_name: str, program_name: str):
        logging.debug(f"Stop app called for {Paths.RUN_DIR.value + script_name}")
        if not script_name.endswith(".sh") and not isBinary(script_name):
            logging.error(f'script_name format is wrong {script_name} must be a ".py", ".sh" or a binary')
            return
        else:
            if isRunning(program_name=program_name):
                result = subprocess.run([Paths.RUN_DIR.value + script_name, "--deactivate"], stderr=subprocess.PIPE)
                logging.info(f"Stopped application: {script_name} succesfully")
            else:
                logging.info(f"Application {script_name} not running so not stopped")

class AppMan(AbstractAppMan):
    def __init__(self):
        buildDirectories()
        self.db: Database = Database()
        self.startActiveApps()

    def ApiRequests(self, request: str, arg: Optional[str] = None):
        if request == "pairs":
            ret = {}
            for name, app in self.db.apps.items():
                ret[name] = [app.run, name]
                ret[app.id] = [app.run, name]
            return ret
        elif request == "list":
            ret = {}
            for name, app in self.db.apps.items():
                ret[name] = app.to_dict()
            return ret
        elif request == "activate":
            self.db.activateApp(arg)
            self.startApp(self.db.apps[arg].run, self.db.apps[arg].program_name)
        elif request == "deactivate":
            self.db.deactivateApp(arg)
            self.stopApp(self.db.apps[arg].run, self.db.apps[arg].program_name)

    def startActiveApps(self):
        logging.info(f"start active apps called")
        for name, app in self.db.apps.items():
            if app.active:
                try:
                    logging.info(f"Launching: {name}, filename: {app.run}")
                    self.startApp(app.run, app.program_name)
                except Exception as e:
                    logging.error(f"Could not execute subprocess to start app: {e}")
        logging.info(f"end of start active apps")
