from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FIXED IMPORT
from backend.app.routes.spam import router as spam_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include router
app.include_router(spam_router)
