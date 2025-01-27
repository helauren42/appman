from fastapi import FastAPI, Request, Response
import uvicorn
import sqlite3
import logging

from const import HOST, PORT, DB_PATH

# GLOBALS
app = FastAPI()
connect = sqlite3.connect(DB_PATH)
cursor: connect.cursor = connect.cursor()

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

@app.get("/")
def home():
    return ("hello world")

@app.post("/addApp/{name}")
def activate(request: Request):
    pass
    

# @app.post("/addApp/{name}")
# def add("")


def main():
    uvicorn.run(app, host=HOST , port=PORT)


if __name__ == "__main__":
    main()