from fastapi import FastAPI

app = FastAPI()

# Code 1: Simple "Hello World" response
'''
@app.get("/")
async def root():
    return {"message": "Hello World"}
'''
#127.0.0.1:8000/"

#Code 2: Print item_id
'''
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id is": item_id}
'''
#127.0.0.1:8000/items/blalba"


#Code 3: Retrieve User Id (Order Matters)
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

# Code 4: Predefined paths
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

# Code 4: Predefined paths
## Query Parameters
'''
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
'''

#127.0.0.1:8000/items/?skip=0&limit=10
### Optional Parameters (Union)
'''
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: int | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
'''
#127.0.0.1:8000/items/blabla?q=4

### Query parameter type conversion
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


# Multiple path and query parameters
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
#127.0.0.1:8000/users/4123/items/shoe?q=blabla&short=1
#127.0.0.1:8000/users/4123/items/shoe