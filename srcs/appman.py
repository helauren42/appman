import uvicorn
import logging
from abc import ABC
import subprocess
from sys import exit

# from const import HOST, PORT, DB_FILE, RUN_DIR
from const import HOST, PORT, Paths
from utils import buildDirectories, isBinary
from db import Database

# GLOBALS

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("../.logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

class AbstractAppMan(ABC):
    def startApp(filename: str):
        logging.debug("Start app called for {filename}")
        if not filename.endswith(".py") and not filename.endswith(".sh") and not isBinary(filename):
            logging.error(f'filename format is wrong {filename} must be a ".py", ".sh" or a binary')
            return
        if filename.endswith(".py"):
            result = subprocess.run(["python3", filename], stderr=subprocess.PIPE, close_fds=True, cwd=RUN_DIR)
        else:
            result = subprocess.run([filename], stderr=subprocess.PIPE, cwd=Paths.RUN_DIR)

class AppMan():
    def __init__(self):
        buildDirectories()
        self.db: Database = Database()
        logging.debug("db built")
        self.startActiveApps()

    def startActiveApps(self):
        for name, app in self.db.apps.items():
            if app.active:
                try:
                    logging.info(f"Launching: {name}, filename: {app.run}")
                    self.startApp(app.run)
                except Exception as e:
                    logging.error(f"Could not execute subprocess to start app: {e}")
