
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ai')))

from core.minio_api import router as minio_router
from ai.analytics import router as ai_router
from ai.advanced_ai import router as advanced_ai_router
from monitoring.monitoring_api import router as monitoring_router
from plugins.plugin_manager import router as plugin_manager_router, plugin_manager

app = FastAPI(title="AI Chart Board Dashboard")

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("dashboard/static/index.html") as f:
        return f.read()

# Include modular routers

# Core APIs
app.include_router(minio_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

# Advanced AI APIs
app.include_router(advanced_ai_router, prefix="/api")

# Monitoring APIs
app.include_router(monitoring_router, prefix="/api")

# Plugin management APIs
app.include_router(plugin_manager_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
