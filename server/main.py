from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.app import api_router
from app.db.db import create_start_table


app = FastAPI(
    title="DnD",
    docs_url=None,      # Disabling Swagger UI
    redoc_url=None,     # Disabling ReDoc
    openapi_url=None
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await create_start_table()


app.include_router(api_router)
