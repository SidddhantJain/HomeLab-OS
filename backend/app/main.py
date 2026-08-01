from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, system, storage, projects, vault, workspace, backup, downloads, documentation, monitoring, alerts



# Auto-create tables for initial boot
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    print(f"Starting {settings.PROJECT_NAME} {settings.VERSION}...")
    from app.core.homelab_core import HomelabCore
    HomelabCore.instance().startup()
    yield
    # Shutdown tasks
    print(f"Shutting down {settings.PROJECT_NAME}...")
    HomelabCore.instance().shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="HomeLab OS v1 Self-Hosted Operating Platform API",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(system.router, prefix=settings.API_V1_STR)
app.include_router(storage.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(vault.router, prefix=settings.API_V1_STR)
app.include_router(workspace.router, prefix=settings.API_V1_STR)
app.include_router(backup.router, prefix=settings.API_V1_STR)
app.include_router(downloads.router, prefix=settings.API_V1_STR)
app.include_router(documentation.router, prefix=settings.API_V1_STR)
app.include_router(monitoring.router, prefix=settings.API_V1_STR)
app.include_router(alerts.router, prefix=settings.API_V1_STR)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
