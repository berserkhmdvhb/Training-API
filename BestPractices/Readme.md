
# 🧠 Complete Best Practices & Architecture Guide for FastAPI Projects

---

## 🧱 1. Project Structure

```
project/
├── app/
│   ├── api/              # APIRouters grouped by version/resource
│   │   └── v1/
│   │       └── items.py
│   ├── core/             # App-wide config, constants, startup, shutdown
│   ├── models/           # ORM models (SQLAlchemy or Tortoise)
│   ├── schemas/          # Pydantic models (request/response)
│   ├── services/         # Business logic
│   ├── repositories/     # Data-access layer (CRUD abstraction)
│   ├── db/               # DB engine/session connection
│   ├── dependencies/     # Custom reusable Depends() logic
│   └── utils/            # Common helper functions
├── tests/                # Unit and integration tests
├── main.py               # FastAPI app entrypoint
├── .env / .env.example   # Environment config
├── requirements.txt
└── README.md
```

✅ Optional: Domain-Driven Design structure with `/domain/item`, `/domain/user`, etc.

---
## 2. 🧠 Coding Best Practices & Clean Code

### ✅ Code Clarity
- Follow **PEP8** formatting.
- Use **type hints** (`str`, `int`, `Annotated`, etc.).
- Use **clear, consistent naming** (e.g., plural route names: `/items/`, not `/item/`).
  

### ✅ Avoid Code Smells (Refactoring Guru):
- **Long functions** → split into smaller helpers.
- **Duplicated logic** → use dependency injection or service layer.
- **Tight coupling** → abstract DB logic into repositories/services.
- **Inconsistent naming** → follow RESTful and Python conventions.
- **God object** → split large classes or files by responsibility.
---
## 🧪 3. Testing


- Override dependencies with `app.dependency_overrides[...]`
- Use `pytest`, `fixtures`, factory functions
- Cover: valid flows, edge cases, auth failures, validation errors
- Use `TestClient` for full request/response testing:

Using `TestClient`, test the following:

  - Routes (status code, response schema)
  - Validation (400s on bad input)
  - Business logic


### ✅ Sample `test_main.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/api/v1/items", json={"name": "Test", "price": 10.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
```

---

## 🧬 4. Dependency Injection (`Depends()`)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    ...
```

- Use for DB session, auth, Pagination/query filter logic
- Chain dependencies: `get_current_user`, then `get_admin_user`
- Improves testability & modularity
- Use in services too (not just routes)

---

## 🧼 5. Clean Code & Design Principles

- Use `Annotated[]`, `Field()`, `BaseModel`
- Avoid:
  - God classes/modules
  - Long functions
  - Duplicate code
- Follow SOLID: Single Responsibility, Open/Closed, etc.
- Keep route handlers thin (delegate to services)
- Consistent naming: plural nouns, snake_case in Python, kebab-case in URLs
    ![31](figures/31.PNG)
    ![32](figures/32.PNG)

  ### ✅ Linting & Formatting
- Use `ruff` for linting and formatting

### ✅ Git & Version Control
- Use GitHub repo for hosting and version tracking
- Write clean commit messages
- Use `.gitignore`

### ✅ CI/CD (Optional for now)
- Add GitHub Actions for:
  - Testing on push
  - Linting/formatting check

---

## 🗂️ 6. Pydantic Usage

```python
class Item(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

    class Config:
        orm_mode = True
```

- Separate `schemas` from `models`
- Use inheritance: `BaseItem`, `ItemCreate`, `ItemRead`
- Use `Config.orm_mode = True` for DB serialization
- Include examples via `Config.schema_extra`

---

## 🔁 7. API Design Best Practices

- Use nouns in paths: `/items/`, `/orders/{order_id}`
    ![34](figures/34.PNG)
- Version APIs: `/api/v1/...`
    ![42](figures/42.PNG)
    ![43](figures/43.PNG)
- * Use **clear query strings** for filtering and sorting:
  * Example: `?sort_by=registered`
  * Example: `?filter=color:blue`
  ![44](figures/44.PNG)
  ![45](figures/45.PNG)
  ![46](figures/46.PNG)
  ![47](figures/47.PNG)
  ![48](figures/48.PNG)
  ![49](figures/49.PNG)
  ![50](figures/50.PNG)  
- Support:
  - Pagination: `?limit=20&offset=0`
    - **Offset-based** (`limit`, `offset`) — simple but can be slow on large datasets
    ![18](figures/18.PNG)
    ![18_2](figures/18_2.PNG)
    ![18_3](figures/18_3.PNG)
    ![18_4](figures/18_4.PNG)
    ![18_5](figures/18_5.PNG)
    ![18_6](figures/18_6.PNG)
    -**Cursor-based** — scalable, tracks changes better
  - Filtering: `?status=active`
  - Sorting: `?sort=-created_at`
- Idempotency for PUT, DELETE:
  -`GET`: naturally idempotent
  - `PUT`, `DELETE`: should be idempotent
  - `POST`: not idempotent by default — implement safeguards (client-generated IDs)
  - `PATCH`: not guaranteed idempotent — document behavior
  ![36](figures/36.PNG)
  ![37](figures/37.PNG)
  ![38](figures/38.PNG)
  ![39](figures/39.PNG)
  ![40](figures/40.PNG)
  ![41](figures/41.PNG)
- Return appropriate status codes

- Use consistent, clear URL patterns:
  - Plural nouns for collections (`/users/`)
  - Forward slashes (`/`) for hierarchy
  - Hyphens (`-`) for multi-word segments
- Keep cross-resource references simple
- Plan for **rate limiting** to protect from abuse and DDoS attacks
    ![51](figures/51.PNG)
    ![52](figures/52.PNG)
    ![53](figures/53.PNG)
    ![54](figures/54.PNG)
---

## 🛡️ 8. Security

- Use `Depends(get_current_user)` for secured endpoints
- Auth options: OAuth2 + JWT, API keys
- Don't expose stack traces
- Validate everything with Pydantic
- CORS: restrict origins in production
- Plan for **rate limiting**:
  - Per-IP, per-user, per-endpoint quotas
  - Example: Free users 1000 requests/day, 20 req/min/IP
- **Security should not be an afterthought:** integrate from the start

  - Enforce authentication/authorization consistently
  - Use HTTPS everywhere
  - Monitor dependencies for CVEs

---

## ⚙️ 9. Config & Environments

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

- Centralize config in `core/config.py`
- Load secrets via `.env`
- Provide `.env.example` for reference
- Inject config with `Depends(get_settings)`

### ✅ Environment Management
- Use `.env` and `pydantic.BaseSettings` for:
  - Secrets
  - DB URIs
  - API keys

### ✅ Config Loader
- Centralize config in a file like `settings.py` or `config.py`


---

## 🚀 10. Performance & Optimization
![2](figures/2.PNG)  

* Use `async def` + `await` for all I/O operations
* Use async DB drivers (SQLAlchemy 2.0+ async, Tortoise ORM)
* Avoid blocking I/O in event loop: use `run_in_threadpool()` where needed
* **Avoid N+1 queries:** use `selectinload()`, efficient joins
  ![13](figures/13.PNG)
  ![14](figures/14.PNG)
  ![15](figures/15.PNG)
* **Enable connection pooling** to avoid repeated DB handshake overhead
    ![6](figures/6.PNG)
    ![7](figures/7.PNG)
    ![8](figures/8.PNG)  
* **Use caching:** Redis, Memcached, or local LRU for frequently accessed data
    ![3](figures/3.PNG)
    ![4](figures/4.PNG)
    ![5](figures/5.PNG)  
* **Pagination:** implement offset-based *and/or* cursor-based pagination (cursor preferred for large dynamic datasets)
* Enable compression (Gzip or Brotli) on large responses
  ![21](figures/21.PNG)
  ![22](figures/22.PNG)
  ![23](figures/23.PNG)
  ![24](figures/24.PNG)
* Use **lightweight JSON serializers** (e.g. `orjson`) for faster JSON encoding
  ![19](figures/19.PNG)
  ![20](figures/20.PNG)
* Use **asynchronous logging** in high-throughput systems to avoid blocking I/O
  ![25](figures/25.PNG)
  ![26](figures/26.PNG)
  ![27](figures/27.PNG)
  ![28](figures/28.PNG)
* Use background tasks for expensive post-response processing
---

## 🧾 11. Logging & Error Handling

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

- Use `logging.config.dictConfig` for structured logs
- For high-performance systems, implement **asynchronous logging** (background log writing)

  - Be aware of slight risk of log loss if app crashes before flush
- Customize error handlers: `HTTPException`, `RequestValidationError`
- Avoid exposing internal stack traces
- Use correlation IDs for tracing requests


---

## 📚 12. Documentation & Developer Experience

- Auto docs via Swagger (`/docs`) and ReDoc (`/redoc`)
- Use:
  - `summary=`, `description=`, `tags=[...]`
  - `response_model=`
- Add examples in Pydantic models
- Disable docs in production if private

---

## 🧩 13. Advanced Features (Optional)

- `BackgroundTasks` for async post-response jobs
- `orjson` or `ujson` for faster JSON encoding
- Middleware: logging, metrics, auth
- Add `repositories/` and `services/` layers for Clean Architecture
- Domain folders (`/domain/user`, etc.) for scaling

---

## ⛔ Common Pitfalls

| Mistake                     | Solution                              |
| --------------------------- | ------------------------------------- |
| One large `main.py`         | Split with APIRouters                 |
| Blocking I/O in async route | Use async or threadpool               |
| Skipping validation         | Use Pydantic + `Field()`              |
| No pagination               | Use `limit`, `offset` or cursor-based |
| Exposed internals           | Customize error messages              |
| Unauthenticated routes      | Secure with `Depends()`               |
| No tests                    | Use `pytest`, `TestClient`            |
| No versioning               | Prefix routes with `/api/v1/`         |
| Wildcard CORS               | Only allow trusted origins            |

## General API Engineering Tips

* Use clear and consistent naming in URLs:
  
  * Plural nouns for collections (`/users/`)
  * Forward slashes (`/`) to indicate hierarchy
  * Hyphens (`-`) instead of underscores for multi-word segments
* Plan for future API versions — adopt versioning from day one
* Document idempotency behavior clearly per endpoint
* Use `.env` files for configuration (e.g. `python-dotenv`, `pydantic.BaseSettings`)
* Use Alembic for DB migrations (if using relational DB)
* Automate CI/CD pipelines — include tests and lint checks
---
