# Initialize
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Form, File, UploadFile, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Literal, Any
from pydantic import BaseModel, Field, EmailStr

from datetime import datetime, time, timedelta
from uuid import UUID

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


#########################################################################################

# Simple "Hello World" response

'''
@app.get("/")
async def root():
    return {"message": "Hello World"}
'''

#127.0.0.1:8000/"

#########################################################################################

# Print item_id

'''
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id is": item_id}
'''

#127.0.0.1:8000/items/blalba"

#########################################################################################

# Retrieve User Id (Order Matters)

'''
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
'''

#127.0.0.1:8000/users/me"
#127.0.0.1:8000/users/blabla"

#########################################################################################

# Predefined paths
## Path Parameters

'''
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
'''

#127.0.0.1:8000/models/alexnet"
#127.0.0.1:8000/models/blalba"

#########################################################################################

# Query Parameters

'''
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
'''

#127.0.0.1:8000/items/?skip=0&limit=10

#########################################################################################

## Optional Parameters (Union)

'''
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: int | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
'''

#127.0.0.1:8000/items/blabla?q=4

#########################################################################################

## Query parameter type conversion

'''
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
'''

#127.0.0.1:8000/items/aaa?q=222&short=True
#127.0.0.1:8000/items/foo?short=true
#127.0.0.1:8000/items/foo?short=yes
#127.0.0.1:8000/items/foo?short=1
#127.0.0.1:8000/items/foo?short=T

#127.0.0.1:8000/items/aaa?q=222

#########################################################################################

# Multiple path and query parameters

'''
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
 '''

#127.0.0.1:8000/users/4123/items/shoe?q=blabla&short=1
#127.0.0.1:8000/users/4123/items/shoe

#########################################################################################

# Request Body
## Create Data Model

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

### POST: Simple Version

'''
@app.post("/items/")
async def create_item(item: Item):
    return item 
'''

### POST: Refined Version

'''
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
'''


## PUT: Request body + path parameters

'''
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
'''

## PUT: Request body + path + query parameters

'''
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
'''

#########################################################################################

# Query Parameters and String Validations

'''
@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
'''

## Additional validation on length of q
### Here we are using Query() because this is a query parameter.
### Path(), Body(), Header(), and Cookie(), that also accept the same arguments as Query().

'''
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$", alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
'''

#127.0.0.1:8000/items/?item-query=blablalba
#127.0.0.1:8000/items/?item-query=fixedquery

#########################################################################################

# Path Parameters and Numeric Validations

##gt: greater than
##ge: greater than or equal
##lt: less than
##le: less than or equal

'''
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
'''

#########################################################################################

# Query Parameter Models
#If you have a group of query parameters that are related, you can create a Pydantic model to declare them.

'''
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
'''

#########################################################################################

# Body
## Multiple Parameters: Mix Path, Query and body parameter

'''
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
'''

## Singular values in body

class User(BaseModel):
    username: str
    full_name: str | None = None
    
'''

@app.put("/items/{item_id}")
async def update_item(
    item_id: int, 
    item: Item, 
    user: User, 
    importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
'''


# By default, singular values are interpreted as query parameters, you don't have to explicitly add a Query
# When * is given as arg, from this point onward, all parameters must be passed as keyword arguments (not positional)

'''
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
'''
#########################################################################################

# Body
## Fields

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

'''
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
'''

# Without Embed

'''
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
'''

# With Embed

'''
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
'''

#########################################################################################

# Body
## Nested Models

class Image(BaseModel):
    url: str
    name: str

### List Fields
### tags are supposed to be unique strings -> set instead of list

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = set()
    image: Image | None = None

'''
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
'''

### Example:

'''
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://exazmple.com/baz.jpg",
        "name": "The Foo live"
    }
}
'''

#########################################################################################

# Declare Request Example Data


## Extra JSON Schema data in Pydantic models¶

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

'''
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
'''

## Field additional arguments 


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])

'''
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
'''

## Body with examples

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

'''
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
'''

#########################################################################################

# Extra Data Types

'''
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
'''

#########################################################################################

# Cookie Parameters

'''
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
'''

## Add data model

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

'''
@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
'''

#########################################################################################

# Header Parameters

'''
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
'''


## Add data model

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

'''
@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
'''

#########################################################################################

# Response Type

## 1. Return Type: Filtered data but no flexibility

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

'''
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
'''

### Doesn't work if the return data type won't be as exactly as declared type (Item).

## 2. response_model Parameter:
### Case where you need or want to return some data that is not exactly what the type declares.
### You could want to return a dictionary or a database object, but declare it as a Pydantic model.
'''
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
'''

## 2. response_model parameter, BaseModel for both input and output
## Filtered data but no tooling support
### Classes are different, so resposne_model is required.
### We don't have support from editor and tools checking return type 

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

'''
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user
'''

## 3. Inheritance
##  est of both worlds: type annotations with tooling support and data filtering.
### We have flexiblity of different objects
### FastAPI will still do data documentation, validation, etc.
### Equipped with converting and filtering the output data to its type declaration.

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str

'''
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
'''

# 4. Return a Response Directly

'''
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})
'''


#########################################################################################

# Extra Models

## Primary example

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

'''
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
'''

## Refined version: use inheritance


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str

'''
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
'''

#########################################################################################

# Receive form fields instead of JSON

'''
@app.post("/login/")
async def login(
                username: Annotated[str, Form()], 
                password: Annotated[str, Form()]
            ):
    return {"username": username}

'''

## Form Models
### Forbid Extra Form Fields with model_config

class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

'''
@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
'''

#########################################################################################

# Request Files

## Byte
## Putting default value makes file uploading optional

'''
@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}
'''

## UploadFile

'''
@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile | None, File(description="A file read as UploadFile")] = None,
):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
'''

#########################################################################################

# Handling Errors

items = {"foo": "The Foo Wrestlers"}

'''
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
'''

## Add custom headers

'''
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
'''

#########################################################################################

# Body: Update

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

'''
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
'''

#########################################################################################

# Body: Patch

'''
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    ###log###
    logger.info(f"Stored model before update: {stored_item_model}")
    #########
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
'''

#########################################################################################

# Dependencies

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

'''
#async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#    return {"q": q, "skip": skip, "limit": limit}

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
'''

# Sub-dependencies

## Function Version

'''
def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}
'''

## Class Version

'''
class QueryExtractor:
    def __call__(self, q: str | None = None) -> str | None:
        return q

class QueryOrCookieExtractor:
    def __init__(self, query_extractor: Annotated[str | None, Depends(QueryExtractor)]):
        self.query_extractor = query_extractor

    def __call__(self, last_query: Annotated[str | None, Cookie()] = None) -> str | None:
        return self.query_extractor or last_query

@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str | None, Depends(QueryOrCookieExtractor)],
):
    return {"q_or_cookie": query_or_default}
'''

# Dependencies in path operation decorators
## Case that you don't need return value of dependency
## But you still need it to be executed/solved 

'''
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
'''

# Global Dependencies

'''
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
'''
`
# Dependencies with yield

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()