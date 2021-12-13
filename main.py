from fastapi import FastAPI
from app.routers.search_info import info_router


app = FastAPI()
app.include_router(info_router)
