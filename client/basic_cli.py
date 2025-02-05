from requests import Response
import requests
import sys
import argparse
import subprocess
from abc import ABC, abstractstaticmethod
import json
from enum import Enum
import logging

HOST = "127.0.0.1"
PORT = 5698

urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.ERROR)

class Parser():
    @abstractstaticmethod
    def print_appman_help():
        print("""appman: A command-line utility for managing Linux applications.

        Usage: appman$ [options] or appman$ <executable> [args...]

        Run an executable:
        appman /path/to/program [arguments...]  (If no options are given)

        Management Options:
        list        Lists all registered applications and their status.
        refresh     Refresh the application list.
        activate <program1> <program2> ....
                    Activate one or more programs.
        deactivate <program1> <program2> ....
                    Deactivate one or more programs.
        help        Display this help message.
        """)

    class parsedMode(Enum):
        APPMAN = 0
        APPLICATION = 1

    @abstractstaticmethod
    def parse(args: list[str]) -> dict[str, dict]:
        struct = {"on":False, "arg": []}
        ret = {"list": struct.copy(),
            "refresh": struct.copy(),
            "activate": struct.copy(),
            "deactivate": struct.copy()
            }
        mode = Parser.parsedMode.APPMAN
        if not args or args[0] == "" or help in args:
            Parser.print_appman_help()
            raise Exception("help")

        if args[0] == "list":
            ret["list"]["on"] = True
        elif args[0] == "refresh":
            ret["refresh"]["on"] = True
        elif args[0] == "activate":
            if len(args) <= 1:
                raise Exception("activate requires arguments")
            ret["activate"]["on"] = True
            ret["activate"]["arg"] = args[1:]
        elif args[0] == "deactivate":
            if len(args) <= 1:
                raise Exception("deactivate requires arguments")
            ret["deactivate"]["on"] = True
            ret["deactivate"]["arg"] = args[1:]
        else:
            return (Parser.parsedMode.APPLICATION, args)
        return (Parser.parsedMode.APPMAN, ret)

class output(ABC):
    @abstractstaticmethod
    def list(response):
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if content == "" or content == "{}":
                print("No applications registered")
                return
            data = json.loads(content)
            for key, value in data.items():
                print("-" * 80)
                print(f"APP: {key}")
                print(f"Run: {value["run"]}")
                print(f"Program Name: {value["program_name"]}")
            if value["active"]:
                print("Status: \033[92mactive\033[0m")
            else:
                print("Status: \033[91minactive\033[0m")
                print(f"Description: {value["description"]}")
            print("-" * 80)
        else:
            print(f'{response.content}')
            print(f"Status code: {response.status_code}")

    @abstractstaticmethod
    def refresh(response):
        if response.status_code == 200:
            print("refresh done succesfully")
        else:
            print(f'{response.content}')
            print(f"Status code: {response.status_code}")

    @abstractstaticmethod
    def activate(response):
        print(f'{response.content.decode('utf-8')}')
        print(f"Status code: {response.status_code}")

    @abstractstaticmethod
    def deactivate(response):
        print(f'{response.content.decode('utf-8')}')
        print(f"Status code: {response.status_code}")

def makeRequest(method: str, url):
    try:
        response = requests.request(method, url)
        print(f"response: {response}")
    except Exception as e:
        print(f"Request failed: {e}")
        raise
    return response

def process_args(args: dict[str, dict]):
    if args["list"]["on"]:
        response = makeRequest("GET", f'http://{HOST}:{PORT}/list')
        output.list(response=response)
    elif args["refresh"]["on"]:
        response = makeRequest("POST", f'http://{HOST}:{PORT}/refresh')
    elif args["activate"]["on"]:
        for arg in args["activate"]["arg"]:
            response = makeRequest("POST", f'http://{HOST}:{PORT}/activate/{arg}')
            output.activate(response=response)
    elif args["deactivate"]["on"]:
        for arg in args["deactivate"]["arg"]:
            response = makeRequest("POST", f'http://{HOST}:{PORT}/deactivate/{arg}')
        output.deactivate(response=response)

