from appman import app, AppMan

@app.get("/")
def home():
    return ("hello world")

@app.post("/activate/{name}")
def activate():
    pass

@app.post("/deactivate/{name}")
def deactivate():
    pass
