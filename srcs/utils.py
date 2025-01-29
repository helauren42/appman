import os
import sqlite3
from const import DB_DIR, DB_PATH, LOG_DIR, BIN_DIR

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
    os.system("mkdir -p " + LOG_DIR)
    os.system("mkdir -p " + DB_DIR)
    os.system("mkdir -p " + BIN_DIR)
