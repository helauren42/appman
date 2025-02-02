from requests import Response
import requests
import sys
import argparse
import subprocess
from abc import ABC, abstractstaticmethod
import json

HOST = "127.0.0.1"
PORT = 5698

def parse():
    parser = argparse.ArgumentParser(prog="appman", description="A command-line utility for appman you app manager for linux applications, official ones and none official ones.")
    parser.add_argument("-l", "--list", action="store_true", help="Lists all the current programs registered on appman, and their current status (active/inactive)")
    parser.add_argument("-r", "--refresh", action="store_true", help="Use refresh after adding a new application to the appman directory")
    parser.add_argument("-a", "--activate", type=str, help="Sets the program to active and appman will run its script when appman is launched")
    parser.add_argument("-d", "--deactivate", type=str, help="Sets the program to inactive and appman will be ignoring its run script")
    return (parser.parse_args(), parser)

class output(ABC):
    @abstractstaticmethod
    def list(response):
        if response.status_code == 200:
            content = response.content.decode('utf-8')
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
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)
    return response

def process_args(args):
    if args.list:
        response = makeRequest("GET", f'http://{HOST}:{PORT}/list')
        output.list(response=response)
    if args.refresh:
        response = makeRequest("POST", f'http://{HOST}:{PORT}/refresh')
    if args.activate:
        response = makeRequest("POST", f'http://{HOST}:{PORT}/activate/{args.activate}')
        output.activate(response=response)
    if args.deactivate:
        response = makeRequest("POST", f'http://{HOST}:{PORT}/activate/{args.deactivate}')

def main():
    args, parser = parse()
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)
    process_args(args)

if __name__ == "__main__":
    main()
