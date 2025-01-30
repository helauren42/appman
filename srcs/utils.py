import os
import sqlite3
# from const import DB_DIR, DB_FILE, LOG_DIR, BIN_DIR, APPS_DIR
from const import Paths
import logging

def isBinary(filename: str, blocksize=1024):
    with open(filename, 'rb') as f:
        chunk = f.read(blocksize)
        if b'\0' in chunk:  # Check for null bytes
            return True
        # Check for high percentage of non-text characters
        text_characters = bytes(range(32, 127)) + b'\n\r\t\b'
        non_text = sum(byte not in text_characters for byte in chunk)
        return non_text / len(chunk) > 0.3

def buildDirectories():
    logging.info("buildDirectories")
    os.system("mkdir -p " + Paths.APPS_DIR.value)
    os.system("mkdir -p " + Paths.LOG_DIR.value)
    os.system("mkdir -p " + Paths.DB_DIR.value)
    os.system("mkdir -p " + Paths.BIN_DIR.value)
