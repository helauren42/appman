from requests import Response
import requests
import sys
import argparse

HOST = "127.0.0.1"
PORT = 5698

resp: Response = requests.get(f'http://{HOST}:{PORT}')

parser = argparse.ArgumentParser(prog="appman", description="A command-line utility for appman you app manager for linux applications, official ones and none official ones.")

parser.add_argument("-l", "--list", type=bool, help="Lists all the current programs registered on appman, and their current status (active/inactive)")
parser.add_argument("-r", "--refresh", type=bool, help="Use refresh after adding a new application to the appman directory")
parser.add_argument("-a", "--activate", type=str, help="sets the program to active and appman will run its script when appman is launched")
parser.add_argument("-d", "--deactivate", type=str, help="sets the program to inactive and appman will be ignoring its run script")


