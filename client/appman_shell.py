from requests import Response
import requests
import sys
import argparse
import subprocess
from abc import ABC, abstractstaticmethod
import json
import signal

from basic_cli import Parser, output, makeRequest, process_args
from const import Paths

PROMPT = "appman$>"
HOST = "127.0.0.1"
PORT = 5698

def sigterm_handler(signum, frame):
    sys.exit(1)

def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    while True:
        print(PROMPT, end=" ")
        read = input().strip()
        mode, parsed = ("", {})
        try:
            mode, parsed = Parser.parse(read.split())
        except Exception as e:
            if e != "help":
                print(f"Error: {e}")
            continue
        if mode == Parser.parsedMode.APPMAN:
            process_args(parsed)
        else:
            try:
                print("path: ", Paths.RUN_DIR.value)
                print("parsed: ", parsed)
                path = Paths.RUN_DIR.value + parsed[0]
                if len(parsed) > 1:
                    cmd = [path] + parsed[1:]
                else:
                    cmd = [path]
                print("cmd: ", cmd)
                result = subprocess.run(cmd, capture_output=True, text=True)
                print(result.stdout, end="")
                print(result.stderr, end="")
                print("\n", end="")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
