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

@app.get("/list")
def list():
    return JSONResponse(status_code=200, content=appman.db.apps)

@app.post("/refresh")
def refresh():
    appman.refresh()
    return Response(status_code=200)

@app.post("/activate/{name}")
def activate():
    try:
        appman.ApiRequests("activate", name) == 400
    except Exception as e:
        return Response(content=f"{name} not found", status_code=400)
    return Response(content=f"{name} activated", status_code=200)

@app.post("/deactivate/{name}")
def deactivate():
    try:
        appman.ApiRequests("deactivate", name) == 400
    except Exception as e:
        return Response(content=f"{name} not found", status_code=400)
    return Response(content=f"{name} deactivated", status_code=200)

def main():
    uvicorn.run(app, host=HOST , port=PORT)

if __name__ == "__main__":
    main()
