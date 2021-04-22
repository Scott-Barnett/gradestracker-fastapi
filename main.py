#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import uvicorn

app = FastAPI()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

from local_config import local_config
import api.models
import api.routes

if __name__ == "__main__":
    if local_config["DEBUG"]:
        print("Starting server in DEBUG mode - Edit local_config.json to change this")
    uvicorn.run("main:app", reload=local_config["DEBUG"])
