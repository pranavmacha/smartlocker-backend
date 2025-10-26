from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, sessions

app = FastAPI(
    title="Smart Locker API",
    description="Backend for Smart Charging Locker",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Flutter app domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Smart Locker API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}