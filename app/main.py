from fastapi import FastAPI
from app.routers import users
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title=settings.PROJECT_NAME)




origins = [
    "http://localhost:3000",  # Frontend URL (e.g., React app running locally)
    "https://yourfrontenddomain.com",  # Add your production frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (like content-type, authorization, etc.)
)



# Include Routers
app.include_router(users.router, prefix="/api/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
