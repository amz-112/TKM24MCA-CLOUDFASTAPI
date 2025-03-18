from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory storage (list of dictionaries)
items = []

# Pydantic Model
class Item(BaseModel):
    id: int
    name: str
    description: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

# Create (POST) - Prevents duplicate entries
@app.post("/add")
def create_item(name: str = Form(...), description: str = Form(...)):
    for item in items:
        if item["name"].lower() == name.lower():  # Check if item already exists
            return {"message": "Item already exists!"}
    
    new_item = {"id": len(items) + 1, "name": name, "description": description}
    items.append(new_item)
    return {"message": "Item added successfully", "item": new_item}

# Read (GET)
@app.get("/items")
def get_items():
    return items

# Update (PUT) - Full Update
@app.put("/update/{item_id}")
def update_item(item_id: int, name: str = Form(...), description: str = Form(...)):
    for item in items:
        if item["id"] == item_id:
            item["name"] = name
            item["description"] = description
            return {"message": "Item updated successfully", "item": item}
    return {"error": "Item not found"}

# Partial Update (PATCH)
@app.patch("/update/{item_id}")
def patch_item(item_id: int, name: str = Form(None), description: str = Form(None)):
    for item in items:
        if item["id"] == item_id:
            if name:
                item["name"] = name
            if description:
                item["description"] = description
            return {"message": "Item updated successfully", "item": item}
    return {"error": "Item not found"}

# Delete (DELETE)
@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    global items
    items = [item for item in items if item["id"] != item_id]
    return {"message": "Item deleted successfully"}
