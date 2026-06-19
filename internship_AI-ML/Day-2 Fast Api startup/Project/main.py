from fastapi import FastAPI
from api.endpoint import router

app = FastAPI()
app.include_router(router)