# Connecting to database from local


## Achieve MVC in FastAPI
- [1](https://stackoverflow.com/questions/64943693/what-are-the-best-practices-for-structuring-a-fastapi-project)
- [2](https://verticalserve.medium.com/building-a-python-fastapi-crud-api-with-mvc-structure-13ec7636d8f2)


## Manual coding

Consider the following simple code for sending a JSON response:

```python
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

The equivalent manual version (and without using decorators) would be following

```python
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()

# Define the route handler function
async def root(request: Request):
    return JSONResponse({"message": "Hello World"})

# Create and add the route explicitly
route = APIRoute(
    path="/",
    endpoint=root,
    methods=["GET"],
    name="root"
)
app.router.routes.append(route)
```
