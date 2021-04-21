from main import app


@app.get("/")
def index():
    return {"message": "hello, world"}
