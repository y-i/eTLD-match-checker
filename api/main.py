import pickle
import os
from typing import Dict
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.domain import DomainResult
from src.checker_trie import ETLDChecker

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

pickle_file = "files/list.pickle"
if os.path.exists(pickle_file):
    with open(pickle_file, "rb") as f:
        checker = pickle.load(f)
else:
    print('initialize checker')
    checker = ETLDChecker()
    checker.initialize_from_file("test/list.dat")
    with open(pickle_file, "wb") as f:
        pickle.dump(checker, f)

@app.get("/")
def read_root() -> HTMLResponse:
    index_html = open("static/index.html", "r").read()
    return HTMLResponse(content=index_html)

@app.get("/check/")
@app.get("/check/{domain}")
def read_check(domain: str) -> DomainResult:
    return checker.check(domain)
