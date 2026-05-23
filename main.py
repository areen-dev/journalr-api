from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from database import Base, engine, get_db
from models import Entry

Base.metadata.create_all(bind=engine)

app = FastAPI()


class EntryCreate(BaseModel):
    content: str


class EntryResponse(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True


@app.get("/entries", response_model=list[EntryResponse])
async def get_function(db=Depends(get_db)):
    content = db.query(Entry).all()
    return content


@app.post("/entries", response_model=EntryResponse)
async def post_function(entry: EntryCreate, db=Depends(get_db)):
    new_entry = Entry(content=entry.content)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@app.delete("/entries/{id}")
async def delete_function(id: int, db=Depends(get_db)):
    entry = db.query(Entry).filter(Entry.id == id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return entry


@app.put("/entries/{id}", response_model=EntryResponse)
async def put_function(id: int, entry: EntryCreate, db=Depends(get_db)):
    db_entry = db.query(Entry).filter(Entry.id == id).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    db_entry.content = entry.content
    db.commit()
    db.refresh(db_entry)
    return db_entry
