from fastapi import Depends, Request, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from main import app
from .models import LocalSession, User
from .schema import Token
from .authentication import PasswordManager, TokenManager


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


def get_user(db, username: str, password: str) -> Optional[User]:
    possible_user = db.query(User).filter(User.username == username).first()
    if possible_user is not None and PasswordManager.verify_password(password, possible_user.password_hash):
        return possible_user


@app.get("/")
def index(db=Depends(get_db)):
    return {"message": "hello, world"}


@app.post("/token", response_model=Token)
def login(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"access_token": TokenManager.generate_token(user.username), "token_type": "bearer"}
