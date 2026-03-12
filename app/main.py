from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import ahp_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://thinh082.github.io",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:5501",
        "https://fe-tuan.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ahp_router)

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}
