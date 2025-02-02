import sqlite3
import subprocess
import os
import logging
import json
from abc import ABC

from const import Paths

class App():
    def __str__(self):
        return (f'active: {self.active}, run: {self.run}, description: {self.description}, settings: {self.settings}')

    def __init__(self, _run, _program_name, _description, _settings=None):
        self.run: str = _run
        self.program_name = _program_name
        self.description: str = _description
        self.active: bool = False
        self.settings: Optional[str] = _settings # .sh
    
    def setActive(self, _active: bool):
        self.active = _active
        
    def to_dict(self):
        return {
            "description":self.description,
            "run":self.run,
            "program_name":self.program_name,
            "active":self.active,
            "settings":self.settings
        }

class AbstractDatabase():
    def initDbCursor(self) -> sqlite3.Cursor:
        self.connect = sqlite3.connect(Paths.DB_FILE.value)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS applications ( \
            name TEXT NOT NULL PRIMARY KEY, \
            active BOOLEAN NOT NULL \
        )")

    def debugPrintTable(self):
        logging.debug("Applications table:")
        rows = self.cursor.execute("SELECT name, active FROM applications ORDER BY name ASC")
        for row in rows:
            logging.debug(f'{row[0]}: {row[1]}')
            
    def findLocalApps(self) -> list[App]:
        self.apps = {}
        result = subprocess.run(["ls -d */"], shell=True, capture_output=True, text=True, cwd=Paths.APPS_DIR.value)
        logging.info(f"Application directories found: {result.stdout}")
        if result.stdout is None or result.stdout == "":
            logging.info(f"Application directories found: {result.stdout}")
        if result.stdout is None or result.stdout == "":
            return None
        app_dir_names = result.stdout.split()
        for app_dir in app_dir_names:
            # get metadata.json file content for every app dir found
            try:
                with open(os.path.join(Paths.APPS_DIR.value + app_dir + "metadata.json"), "r") as file:
                    data = json.load(file)
                    logging.debug(f"metadata: {data}")
                    if "run" not in data or "name" not in data or "description" not in data:
                        logging.warning(f'metadata.json format not valid, could not find one of "run", "name", "description" elements')
                    settings = None if "settings" not in data else data["settings"]
                    app = App(data["run"], data["program_name"], data["description"], settings)
                    name = data["name"]
                    if self.apps.get(name) is not None:
                        logging.warning(f"found duplicate app name: {name}")
                    self.apps[name] = app
            except Exception as e:
                logging.warning(f"metdata.json error: {e}")
                logging.warning(f"metdata.json error: {e}")
                continue
        if len(self.apps) > 0:
            return self.apps
        if len(self.apps) > 0:
            return self.apps
        return None

class Database(AbstractDatabase):
    def __str__(self):
        ret = ""
        for key, app in self.apps.items():
            ret += f'{key}: {str(app)} + "\n"'
        return ret

    def __str__(self):
        ret = ""
        for key, app in self.apps.items():
            ret += f'{key}: {str(app)} + "\n"'
        return ret

    def __init__(self):
        self.connect: sqlite3.Connection
        self.cursor: sqlite3.Cursor
        self.apps: dict[str, App] = {}

        self.initDbCursor()
        self.updateApps()
        logging.info(f'Apps: {self.apps}')
        self.debugPrintTable()
    
    def activateApp(self, name: str):
        if self.apps.get(name) is None:
            logging.error("Wrong app name, app not found, could not ativate")
            raise Exception("App not found")
        if self.apps[name].active == True:
            logging.error(f"{name}: already active")
            raise Exception("Already active")
        logging.info("setting {name} to  True")
        self.apps[name].setActive(True)
        self.initDbCursor()
        print("PRE activate app:")
        self.debugPrintTable()
        self.cursor.execute("UPDATE applications SET name = ?, active = ?", (name, True))
        self.connect.commit()

    def deactivateApp(self, name: str):
        if name in self.apps:
            self.apps[name].setActive(False)
        else:
            logging.error("Wrong app name, app not found, could not ativate")
            raise Exception("App not found")

    def updateApps(self):
        self.findLocalApps() # updates self.apps with current local apps
        self.cursor.execute("SELECT name, active FROM applications ORDER BY name ASC")
        rows = self.cursor.fetchall()
        db_app_names = []
        for row in rows:
            print(f"ROW: {row}")
            if row[0] not in self.apps:
                logging.info(f"Deleting {row[0]} from db")
                self.cursor.execute("DELETE FROM applications WHERE name = ?", (row[0],))
                continue
            db_app_names.append(row[0])
            if row[1] == 1:
                self.apps[row[0]].setActive(True)
            else:
                self.apps[row[0]].setActive(False)
        for app_name in self.apps:
            if app_name not in db_app_names:
                logging.debug(f"Inserting {app_name} into db")
                self.cursor.execute("INSERT INTO applications (name, active) VALUES (?, ?)", (app_name, False))
            self.connect.commit()
