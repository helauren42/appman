from requests import Response
import requests
import sys
import argparse
import subprocess
from abc import ABC, abstractstaticmethod
import json
import signal
import logging

from basic_cli import Parser, output, makeRequest, process_args
from const import Paths, HOST, PORT, PROMPT, GOODBYE_MSG

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(Paths.LOG_DIR.value + "cli.log", mode="w"),
        logging.StreamHandler()
    ]
)

def handler(signum, frame):
    print(GOODBYE_MSG)
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def main():
    print("Welcome to AppMan your favourite app manager!")
    while True:
        print(PROMPT, end=" ")
        try:
            read = input().strip()
        except:
            print(GOODBYE_MSG)
            sys.exit(0)
        if read == "clear":
            res = subprocess.run(["clear"], capture_output=True, text=True)
            if res.stdout is not None:
                print(res.stdout, end="")
            if res.stderr is not None:
                print(res.stderr, end="")
            print("")
            continue
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
                path = Paths.RUN_DIR.value + parsed[0]
                if len(parsed) > 1:
                    cmd = [path] + parsed[1:]
                else:
                    cmd = [path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.stdout is not None:
                    print(result.stdout, end="")
                if result.stderr is not None:
                    print(result.stderr)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
