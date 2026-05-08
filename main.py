from fastapi import FastAPI

from storage import load_entries, save_entries

app = FastAPI()


@app.get("/entries")
def my_func():
    return load_entries()
