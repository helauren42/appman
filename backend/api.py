import uvicorn
import logging

from utils import isBinary
from const import HOST, PORT, Paths
from appman import AppMan
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

app = FastAPI()
appman: AppMan = AppMan()

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(Paths.LOG_DIR.value + ".logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

@app.get("/help")
def home():
    logging.info("request to /help")
    return ("hello world")

@app.get("/list")
def list():
    logging.info("request to /list")
    return JSONResponse(status_code=200, content=appman.ApiRequests("list"))

@app.post("/refresh")
def refresh():
    global appman
    logging.info("request to /refresh")
    try:
        appman = AppMan()
    except Exception as e:
        return Response(status_code=500, content=f"{e}")
    return Response(status_code=200)

@app.post("/activate/{name}")
def activate(name: str):
    logging.info(f"request to /activate/{name}")
    try:
        appman.ApiRequests("activate", name)
    except Exception as e:
        return Response(content=f"Error activating {name}: {e}", status_code=400)
    return Response(content=f"{name} activated", status_code=200)

@app.post("/deactivate/{name}")
def deactivate(name: str):
    logging.info(f"request to /deactivate/{name}")
    try:
        appman.ApiRequests("deactivate", name)
    except Exception as e:
        return Response(content=f"{name}: {e}", status_code=400)
    return Response(content=f"{name} deactivated", status_code=200)

def main():
    uvicorn.run("api:app", host=HOST , port=PORT, reload=True)

if __name__ == "__main__":
    main()
