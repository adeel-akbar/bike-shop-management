from fastapi import FastAPI

from .routers import bikes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(bikes.router)