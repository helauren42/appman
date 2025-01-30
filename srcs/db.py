import sqlite3
import subprocess
import os
import logging

from const import Paths

class App():
    def __init__(self, _directory, _name, _description, _settings):
        directory: str = _directory
        name: str = _name
        description: str = _description
        settings [Optional[str]] = _settings # .sh

class Database():
    def __init__(self):
        self.initDbCursor()
        self.apps: Optional[list[App]] = self.findApps()
        # self.app_names = list[str]

    # def findAppNames(self) -> None:
    #     self.cursor.execute("SELECT appname FROM applications")
    #     self.app_names = self.cursor.fetchall()

    def findApps(self) -> list[App]:
        # result = subprocess.run(["ls", "-d", "*/"], shell=True, capture_output=True, text=True, cwd=Paths.APPS_DIR.value)
        result = subprocess.run(["ls -d */"], shell=True, capture_output=True, text=True, cwd=Paths.APPS_DIR.value)
        logging.info(f"Application directories found: {result}")
        if result.stdout is None or result.stdout.strip() == "":
            return None
        app_dir_names = result.stdout.split()
        for app_dir in app_dir_names:
            # get metadata.json file content
            try:
                with open(Paths.APPS_DIR.value + app_dir + "metadata.json", "r") as file:
                    pass
            except Exception as e:
                logging.warning(f"metdata.json not found inside {Paths.APPS_DIR.value + app_dir}")
                continue
        return None

    def initDbCursor(self) -> sqlite3.Cursor:
        self.connect = sqlite3.connect("../data/appman.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS applications ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            appname TEXT NOT NULL, \
            file TEXT NOT NULL, \
            active BOOLEAN NOT NULL \
        )")
