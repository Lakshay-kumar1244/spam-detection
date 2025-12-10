from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.spam import router as spam_router

app = FastAPI()

# Enable CORS (safe for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(spam_router)
