from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app import crud, database, models, schema

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    database.create_tables()

@app.get("/")
async def root():
    return RedirectResponse(url="/items/")

@app.get("/items/")
async def get_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/")
async def create_item(item: schema.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db, item)
    return db_item

@app.put("/items/{item_id}")
async def update_item(item_id: int, updated_item: schema.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = crud.update_item(db, db_item, updated_item)
    return updated_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, db_item)
    return {"message": "Item deleted successfully"}