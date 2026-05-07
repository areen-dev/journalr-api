from fastapi import FastAPI

app = FastAPI()


@app.get("/entries")
def my_func():
    return [{"id": 1, "content": "my first entry"}]
