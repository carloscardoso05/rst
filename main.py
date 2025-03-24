from fastapi import FastAPI

from api.routes import files
from lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(files.router, prefix="/files")