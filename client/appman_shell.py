from requests import Response
import requests
import sys
import argparse
import subprocess
from abc import ABC, abstractstaticmethod
import json
import signal
import logging

from basic_cli import Parser, output, makeRequest, process_args, getPairs
from const import Paths, HOST, PORT, PROMPT, GOODBYE_MSG

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(Paths.LOG_DIR.value + "cli.log", mode="w"),
        logging.StreamHandler()
    ]
)

def handler(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handler)
    
pairs = {}    

def getCmd(parsed: list) -> str:
    global pairs
    run_file = parsed[0]
    if run_file in pairs:
        run_file = pairs[run_file]
    path = Paths.RUN_DIR.value + run_file
    if len(parsed) > 1:
        cmd = [path] + parsed[1:]
    else:
        cmd = [path]
    return " ".join(cmd)

def main():
    global pairs
    print("Welcome to AppMan your favourite app manager!")
    pairs = getPairs()
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
            if str(e) != "help":
                print(f"Error: {e}")
            continue
        if mode == Parser.parsedMode.APPMAN:
            process_args(parsed)
        else:
            try:
                pairs = getPairs()
                cmd = getCmd(parsed)
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout is not None:
                    print(result.stdout, end="")
                if result.stderr is not None:
                    print(result.stderr)
            except Exception as e:
                print("Error: Not a valid appman command")
                print(f"{e}")

if __name__ == "__main__":
    main()
