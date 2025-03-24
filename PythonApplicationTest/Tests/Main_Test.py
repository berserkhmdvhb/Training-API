from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Form, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Literal
from pydantic import BaseModel, Field
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Pydantic model with validations
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(..., gt=0)
    tax: float | None = Field(default=None, ge=0)


# Create item from request body
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        item_dict["price_with_tax"] = item.price + item.tax
    return item_dict


# Update item with path and query param
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to update", ge=1)],
    item: Item,
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$", alias="item-query")] = None
):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result["q"] = q
    return result


# Read item using path and query param
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$", alias="item-query")] = None
):
    item = {"item_id": item_id}
    if q:
        item["q"] = q
    return item


# Literal query parameter example
@app.get("/status/")
async def get_status(
    status: Annotated[Literal["active", "inactive", "archived"], Query(description="Filter by status")] = "active"
):
    return {"status": status}


# Form data example
@app.post("/submit-form/")
async def submit_form(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    return {"username": username}


# File upload example
@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}


# Cookie example
@app.get("/cookie/")
async def read_cookie(my_cookie: Annotated[str | None, Cookie()] = None):
    return {"cookie": my_cookie}


# Header example with HTTPException
@app.get("/protected/")
async def protected_route(token: Annotated[str | None, Header()] = None):
    if token != "expected-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Welcome!"}
