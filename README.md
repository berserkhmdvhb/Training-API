# Connecting to database from local

## FastAPI Flow Local
### Overview

```mermaid
graph TD
    A["🧑‍💻 Browser / Client<br/>Example: 127.0.0.1:8000"]
    B["🌀 Uvicorn<br/>ASGI Server"]
    C["🚀 FastAPI App"]
    D["📦 Route Handler<br/>@app.get('/')"]
    E["📤 JSON Response"]

    A --> B
    B --> C
    C --> D
    D --> C
    C --> E
    E --> B
    B --> A
```
### Detailed

```mermaid
sequenceDiagram
    autonumber
    participant Browser
    participant OS
    participant Uvicorn as Uvicorn (ASGI Server)
    participant FastAPI
    participant App as Your Python Function

    Note over Browser: User visits http://127.0.0.1:8000/

    Browser->>OS: Send HTTP GET request to 127.0.0.1:8000
    OS->>Uvicorn: Deliver TCP packet with HTTP request

    Note over Uvicorn: Uvicorn listens on 127.0.0.1:8000
    Uvicorn->>Uvicorn: Parse HTTP method and path
    Uvicorn->>FastAPI: Call FastAPI ASGI app with scope & receive/send

    FastAPI->>FastAPI: Match route (GET /)
    FastAPI->>FastAPI: Validate path/query/body with type hints
    FastAPI->>App: Call Python function (e.g. root())

    App-->>FastAPI: Return Python dict (e.g. {"message": "Hello"})

    FastAPI->>FastAPI: Convert return value to JSON
    FastAPI->>Uvicorn: Send response body, headers, status

    Uvicorn->>OS: Build raw HTTP response
    OS->>Browser: Deliver HTTP response over TCP

    Browser->>Browser: Render JSON result in tab

    Note over Browser,App: Entire flow is local on 127.0.0.1

```


## Underlying code

FastAPI stiches multiple libraries together, such as Starlette, Pydantic, Typing, etc.
In this structure, the decorator `@app.get("/")` from FastAPI is equivalent to `Route("/", root, methods=["GET"])` in Starlette.
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

## Resources
- [Best Practices (MVC)](https://stackoverflow.com/questions/64943693/what-are-the-best-practices-for-structuring-a-fastapi-project)
- [Achieve MVC in FastAPI](https://verticalserve.medium.com/building-a-python-fastapi-crud-api-with-mvc-structure-13ec7636d8f2)
- [MVC pattern template](https://github.com/iam-abbas/FastAPI-Production-Boilerplate)
- [Minimalistic but professional template](https://github.com/luchog01/minimalistic-fastapi-template)
- [sqlmodel library: for patching SQLAlchemy with Pydantic](https://github.com/fastapi/sqlmodel)
- [sqlmodel library docs](https://sqlmodel.tiangolo.com/)
