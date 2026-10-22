from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, bikes, sales, stats

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://motodesk.pages.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(bikes.router)
app.include_router(auth.router)
app.include_router(sales.router)
app.include_router(stats.router)