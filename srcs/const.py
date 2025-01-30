import enum
import subprocess
import os

HOST = "127.0.0.1"
PORT = 5698

HOME_DIR = os.path.expanduser("~")

# DIR AND FILE RELATIVE PATHS TO SRCS/

class Paths(enum.Enum):
    APP_ROOT = os.path.join(HOME_DIR + "/.local/appman")
    BIN_DIR = os.path.join(APP_ROOT + "/bin/")
    APPS_DIR = os.path.join(APP_ROOT + "/apps/")
    SETTINGS_DIR = os.path.join(APP_ROOT + "/settings/")

    LOG_DIR = os.path.join(APP_ROOT + "/logger/")
    DB_DIR = os.path.join(APP_ROOT + "/data/")
    DB_FILE = os.path.join(APP_ROOT + "/data/appman.db")
