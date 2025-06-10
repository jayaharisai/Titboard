from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from router import api_router
import os

app = FastAPI()

origins = [
    "http://localhost:3000",   # React dev server example
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    # Add other domains or "*" for all (not recommended for prod)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single API mount point
app.include_router(api_router, prefix="/api")

# Serve React frontend
app.mount("/", StaticFiles(directory="client/build", html=True), name="react")

@app.get("/{full_path:path}")
def react_fallback(full_path: str):
    return FileResponse(os.path.join("client/build", "index.html"))
