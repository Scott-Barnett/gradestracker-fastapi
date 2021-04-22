from fastapi import Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from main import app
from .models import LocalSession, User


@app.middleware("http")
async def middleware(request: Request, call_next) -> Response:
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = LocalSession()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.get("/")
def index(db=Depends(get_db)):
    return {"message": "hello, world"}
