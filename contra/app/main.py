"""FastAPI Application entrypoint for Project Contra."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contra.app.api.routes import router
from contra.app.core.config import settings

app = FastAPI(
    title="Contra: Adversarial Research & Trial Engine",
    description="A research team that argues with itself. Evidence ledgers, adversarial cross-examination, and calibrated falsifiable verdicts.",
    version="1.0.0"
)

# Enable CORS for Next.js / Vite web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Contra - A research team that argues with itself",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("contra.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
