from fastapi import FastAPI

from .routers import auth, bikes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(bikes.router)
app.include_router(auth.router)