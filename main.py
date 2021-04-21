#!/usr/bin/env python3

from fastapi import FastAPI
import uvicorn
import json

with open("local_config.json") as json_file:
    local_config = json.load(json_file)

app = FastAPI()

import api.models
import api.routes

if __name__ == "__main__":
    if local_config["DEBUG"]:
        print("Starting server in DEBUG mode - Edit local_config.json to change this")
    uvicorn.run("main:app", reload=local_config["DEBUG"])
