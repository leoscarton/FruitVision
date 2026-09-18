from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import items

app = FastAPI(title="Fruit Vision")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)


@app.get("/health")
def health():
    return {"status": "ok"}