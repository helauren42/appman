import uvicorn
import logging

from const import HOST, PORT, Paths
from db import Database
from appman import app, AppMan
from utils import buildDirectories, isBinary

@app.get("/")
def home():
    return ("hello world")

@app.post("/activate/{name}")
def activate():
    pass

@app.post("/deactivate/{name}")
def deactivate():
    pass

def main():
    appman: AppMan = AppMan()
    uvicorn.run(app, host=HOST , port=PORT)

if __name__ == "__main__":
    main()
