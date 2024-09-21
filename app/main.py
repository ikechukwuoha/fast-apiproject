from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import users
import logging
import os
from app.internal.adminRouter import adminRouters
from app.internal.adminRouter.authorization_routes import group, permisions, roles
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import permissions_collection, default_permissions



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

# Include Admin Routers
app.include_router(adminRouters.router, prefix="/api/admin", tags=["adminRouter"])


# Include Admin Routers
app.include_router(group.router, prefix="/api/admin/authorization", tags=["group"])
# Include Admin Routers
app.include_router(roles.router, prefix="/api/admin/authorization", tags=["roles"])
# Include Admin Routers
app.include_router(permisions.router, prefix="/api/admin/authorization", tags=["permissions"])




# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to initialize permissions
async def initialize_permissions():
    # Fetch all permissions from the database
    existing_permissions = await permissions_collection.find().to_list(length=100)

    # Use '_id' for existing permissions
    existing_permissions_ids = {perm["name"] for perm in existing_permissions}


    # Identify new permissions that are not already in the database
    new_permissions = [
        {
            "name": perm["name"],
            "description": perm["description"]
        }
        for perm in default_permissions
        if perm["name"] not in existing_permissions_ids
    ]

    if new_permissions:
        # Insert new permissions into the database
        await permissions_collection.insert_many(new_permissions)
        logger.info(f"Inserted {len(new_permissions)} new permissions.")
    else:
        logger.info("All permissions already exist.")

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.add_event_handler("startup", initialize_permissions)  # Trigger initialization in the background
    yield

# Example route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the app!"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
