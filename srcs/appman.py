from fastapi import FastAPI, Request, Response, Query
import uvicorn
import sqlite3
import logging
from abc import ABC
import subprocess
from sys import exit

from const import HOST, PORT, DB_PATH, BIN_DIR
from utils import buildDirectories, isBinary
from db import Database

# GLOBALS
app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("../.logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

class AbstractAppMan(ABC):
    def startApp(FILE: str):
        if not FILE.endswith(".py") and not FILE.endswith(".sh") and not isBinary(FILE):
            logging.error(f'File format is wrong {FILE} must be a ".py", ".sh" or a binary')
            return
        if FILE.endswith(".py"):
            result = subprocess.run(["python3", FILE], stderr=subprocess.PIPE, close_fds=True, cwd=BIN_DIR)
        else:
            result = subprocess.run([FILE], stderr=subprocess.PIPE, cwd=BIN_DIR)

class AppMan():
    def __init__(self):
        buildDirectories()
        self.db: Database = Database()
        self.db.findApps()
        self.startActiveApps(self.db.app_names)

    def startActiveApps(apps: list[str]):
        for app in apps:
            try:
                startApp(app)
            except Exception as e:
                logging.error(f"Could not execute subprocess to start app: {e}")

def main():
    appman: AppMan = AppMan
    startActiveApps()
    uvicorn.run(app, host=HOST , port=PORT)

if __name__ == "__main__":
    main()
