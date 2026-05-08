from fastapi import FastAPI
from pydantic import BaseModel

from storage import load_entries, save_entries

app = FastAPI()


class Entry(BaseModel):
    content: str


@app.get("/entries")
def get_function():
    return load_entries()


@app.post("/entries")
def post_function(entry: Entry):
    entries = load_entries()
    new_entries = {"id": len(entries) + 1, "content": entry.content}
    entries.append(new_entries)
    save_entries(entries)
    return new_entries
