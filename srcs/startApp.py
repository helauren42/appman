import subprocess
from sys import argv, exit
import logging

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

def is_binary(filename, blocksize=1024):
    with open(filename, 'rb') as f:
        chunk = f.read(blocksize)
        if b'\0' in chunk:  # Check for null bytes
            return True
        # Check for high percentage of non-text characters
        text_characters = bytes(range(32, 127)) + b'\n\r\t\b'
        non_text = sum(byte not in text_characters for byte in chunk)
        return non_text / len(chunk) > 0.3

FILE = argv[1]

if not FILE.endswith(".py") and not FILE.endswith(".sh") and not is_binary(FILE):
    print("File format is wrong")
    sys.exit(1)

if FILE.endswith(".py"):
    result = subprocess.Popen(["python3", FILE], stderr=subprocess.PIPE, close_fds=True)
    # if len(result.stderr.decode()) == 0:
        # exit(0)
else:
    result = subprocess.run([FILE], stderr=subprocess.PIPE)


