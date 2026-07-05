from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import *
from app.api.routes import addition, subtraction, multiplication, division

# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/dummy-route")
async def dummy_route():
    return "Dummy route."


app.include_router(addition.router)
app.include_router(subtraction.router)
app.include_router(multiplication.router)
app.include_router(division.router)