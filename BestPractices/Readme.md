
# 🧠 Complete Best Practices & Architecture Guide for FastAPI Projects

This guide combines:
- ✅ Your earlier best practices
- ✅ FastAPI official documentation
- ✅ GitHub templates (minimalistic & production-ready)
- ✅ StackOverflow + blog community insights
- ✅ Refactoring.Guru patterns and code smell practices
- ✅ REST API conventions from real-world APIs

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

## 🧪 2. Testing Best Practices

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/api/v1/items", json={"name": "Test", "price": 10.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
```

- Override dependencies with `app.dependency_overrides[...]`
- Use `pytest`, `fixtures`, factory functions
- Cover: valid flows, edge cases, auth failures, validation errors
- Use `TestClient` for full request/response testing

---

## 🧬 3. Dependency Injection (`Depends()`)

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

- Use for DB session, auth, pagination
- Chain dependencies: `get_current_user`, then `get_admin_user`
- Improves testability & modularity
- Use in services too (not just routes)

---

## 🧼 4. Clean Code & Design Principles

- Use `Annotated[]`, `Field()`, `BaseModel`
- Avoid:
  - God classes/modules
  - Long functions
  - Duplicate code
- Follow SOLID: Single Responsibility, Open/Closed, etc.
- Keep route handlers thin (delegate to services)
- Consistent naming: plural nouns, snake_case in Python, kebab-case in URLs

---

## 🗂️ 5. Pydantic Usage

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

## 🔁 6. API Design Best Practices

- Use nouns in paths: `/items/`, `/orders/{order_id}`
- Version APIs: `/api/v1/...`
- Support:
  - Pagination: `?limit=20&offset=0`
  - Filtering: `?status=active`
  - Sorting: `?sort=-created_at`
- Idempotency for PUT, DELETE
- Return appropriate status codes

---

## 🛡️ 7. Security

- Use `Depends(get_current_user)` for secured endpoints
- Auth options: OAuth2 + JWT, API keys
- Don't expose stack traces
- Validate everything with Pydantic
- CORS: restrict origins in production
- Rate limit public APIs

---

## ⚙️ 8. Config & Environments

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

---

## 🚀 9. Performance & Optimization

- Use `async def` + await for all I/O
- Use async DB (SQLAlchemy 2.0+, Tortoise)
- `run_in_threadpool()` for sync calls
- Avoid N+1: use `selectinload()`, join queries
- Enable GZip/Brotli compression
- Paginate everything
- Use Redis or `lru_cache` for caching

---

## 🧾 10. Logging & Error Handling

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
- Customize error handlers: `HTTPException`, `RequestValidationError`
- Avoid exposing internal stack traces
- Use correlation IDs for tracing requests

---

## 📚 11. Documentation & Developer Experience

- Auto docs via Swagger (`/docs`) and ReDoc (`/redoc`)
- Use:
  - `summary=`, `description=`, `tags=[...]`
  - `response_model=`
- Add examples in Pydantic models
- Disable docs in production if private

---

## 🧩 12. Advanced Features (Optional)

- `BackgroundTasks` for async post-response jobs
- `orjson` or `ujson` for faster JSON encoding
- Middleware: logging, metrics, auth
- Add `repositories/` and `services/` layers for Clean Architecture
- Domain folders (`/domain/user`, etc.) for scaling

---

## ⛔ Common Pitfalls

| Mistake | Solution |
|--------|----------|
| One large `main.py` | Split with APIRouters |
| Blocking I/O in async route | Use async or threadpool |
| Skipping validation | Use Pydantic + `Field()` |
| No pagination | Use `limit`, `offset` |
| Exposed internals | Customize error messages |
| Unauthenticated routes | Secure with `Depends()` |
| No tests | Use `pytest`, `TestClient` |
| No versioning | Prefix routes with `/api/v1/` |
| Wildcard CORS | Only allow trusted origins |

---
