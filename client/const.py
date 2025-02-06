import enum
import subprocess
import os
import logging

HOST = "127.0.0.1"
PORT = 5698
PROMPT = "appman$>"
GOODBYE_MSG = "Goodbye, see you later!"


HOME_DIR = os.path.expanduser("~")

class Paths(enum.Enum):
    APP_ROOT = os.path.join(HOME_DIR + "/.local/appman")
    LOG_DIR = os.path.join(APP_ROOT + "/logger/")
    DB_DIR = os.path.join(APP_ROOT + "/data/")
    DB_FILE = os.path.join(APP_ROOT + "/data/appman.db")

    RUN_DIR = os.path.join(APP_ROOT + "/run/")
    APPS_DIR = os.path.join(APP_ROOT + "/apps/")
    SETTINGS_DIR = os.path.join(APP_ROOT + "/settings/")
