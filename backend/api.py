import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

from utils import isBinary
from const import HOST, PORT, Paths
from appman import AppMan

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(Paths.LOG_DIR.value + "logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

uvicorn_logger = logging.getLogger("fastapi")
uvicorn_logger.setLevel(logging.DEBUG)
uvicorn_logger.addHandler(logging.FileHandler(Paths.LOG_DIR.value + "logger.log", mode="w"))
uvicorn_logger.addHandler(logging.StreamHandler())

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.DEBUG)
uvicorn_logger.addHandler(logging.FileHandler(Paths.LOG_DIR.value + "logger.log", mode="w"))
uvicorn_logger.addHandler(logging.StreamHandler())

uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_error_logger.setLevel(logging.DEBUG)
uvicorn_error_logger.addHandler(logging.FileHandler(Paths.LOG_DIR.value + "logger.log", mode="w"))
uvicorn_error_logger.addHandler(logging.StreamHandler())

logging.info("logger initialized")

appman: AppMan = AppMan()
app = FastAPI()

@app.get("/pairs")
def home():
    logging.info("get request to /pairs")
    return JSONResponse(status_code=200, content=appman.ApiRequests("pairs"))

@app.get("/list")
def list():
    logging.info("get request to /list")
    return JSONResponse(status_code=200, content=appman.ApiRequests("list"))

@app.post("/refresh")
def refresh():
    global appman
    logging.info("post request to /refresh")
    try:
        appman = AppMan()
    except Exception as e:
        return Response(status_code=500, content=f"{e}")
    return Response(status_code=200)

@app.post("/activate/{name}")
def activate(name: str):
    logging.info(f"post request to /activate/{name}")
    try:
        appman.ApiRequests("activate", name)
    except Exception as e:
        return Response(content=f"Error activating {name}: {e}", status_code=400)
    return Response(content=f"{name} activated", status_code=200)

@app.post("/deactivate/{name}")
def deactivate(name: str):
    logging.info(f"post request to /deactivate/{name}")
    try:
        appman.ApiRequests("deactivate", name)
    except Exception as e:
        return Response(content=f"{name}: {e}", status_code=400)
    return Response(content=f"{name} deactivated", status_code=200)

def main():
    logging.info(f"starting api at {HOST}:{PORT}")
    uvicorn.run("api:app", host=HOST , port=PORT, reload=True, log_config=None)

if __name__ == "__main__":
    main()
