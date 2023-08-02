import os
import sys

sys.path.append(os.path.realpath(".."))
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware import Middleware
from datetime import datetime
from logging_module import logger
from fastapi.staticfiles import StaticFiles
from routers import customer_router
from database import engine
from auth_layer.task_app.task_app_schemas.customer_schema import Base




middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


app = FastAPI(middleware=middleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(customer_router.router)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)
    logger.debug("App startup: " + str(datetime.now()))
