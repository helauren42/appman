import uvicorn
import logging

from db import Database
from utils import buildDirectories, isBinary
from const import HOST, PORT, Paths
from appman import AppMan
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

app = FastAPI()
appman: AppMan = AppMan()

@app.get("/")
def home():
    return ("hello world")

@app.get("/activate/list")
def list():
    return JSONResponse()

@app.post("/activate/{name}")
def activate():
    pass

@app.post("/deactivate/{name}")
def deactivate():
    pass

def main():
    uvicorn.run(app, host=HOST , port=PORT)

if __name__ == "__main__":
    main()
