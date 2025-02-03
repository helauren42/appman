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
    print("sigterm handler called")
    print(f"fram: {frame}")
    sys.exit(1)

def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    while True:
        print(PROMPT, end=" ")
        read = input().strip()
        mode, parsed = ("", {}) 
        try:
            mode, parsed = Parser.parse(read.split())
            print(f"type of parsed: {type(parsed)}")
        except Exception as e:
            if e != "help":
                print(f"Error: {e}")
            continue
        print(f"mode: {mode}")
        if mode == Parser.parsedMode.APPMAN:
            if parsed["list"]["on"] == True:
                print("list is on")
            else:
                print("list is off")
            process_args(parsed)
        else:
            try:
                result = subprocess.run(parsed, capture_output=True, text=True, cwd=Paths.APPS_DIR.value)
                print(result.stdout, end="")
                print(result.stderr, end="")
                print("\n", end="")
            except Exception as e:
                print(f"Error: {e}")         

if __name__ == "__main__":
    main()
