from app.lib.init_db import init_db
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from app.lib.response import prepare_template_response
from app.routers import sourcedata_router, analytics_router, crud_router


@asynccontextmanager
async def setup(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=setup)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", tags=["Landing Page"])
async def index(request: Request):
    return prepare_template_response(request=request)


app.include_router(sourcedata_router, tags=["Data Source"])
app.include_router(crud_router, tags=["Crud Operations"])
app.include_router(analytics_router, tags=["Data Analytics"])
