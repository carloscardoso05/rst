from contextlib import asynccontextmanager

from fastapi import FastAPI


def on_startup(app: FastAPI):
    print("Starting up...")


def on_shutdown(app: FastAPI):
    print("Shutting down...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup(app)
    yield
    on_shutdown(app)
