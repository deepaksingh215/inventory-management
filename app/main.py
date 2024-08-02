from fastapi import FastAPI
from routers import router
import models
from db import engine

# from loguru import logger

app = FastAPI()

# logger.add("file.log", rotation="500 MB")
models.Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api/v1")