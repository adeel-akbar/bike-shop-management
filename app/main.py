from fastapi import FastAPI

from .routers import auth, bikes, sales, stats

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(bikes.router)
app.include_router(auth.router)
app.include_router(sales.router)
app.include_router(stats.router)