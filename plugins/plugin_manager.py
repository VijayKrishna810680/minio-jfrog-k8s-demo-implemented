from fastapi import APIRouter, Request
from typing import Callable, Dict
import importlib
import os

class PluginManager:
    """
    Simple plugin manager for dynamic loading and registration of plugins.
    Plugins must define a 'register' function that takes the FastAPI app as argument.
    """
    def __init__(self, plugin_folder: str = "plugins"):
        self.plugin_folder = plugin_folder
        self.plugins: Dict[str, Callable] = {}

    def discover_plugins(self):
        for fname in os.listdir(self.plugin_folder):
            if fname.endswith(".py") and not fname.startswith("__"):
                name = fname[:-3]
                self.plugins[name] = None

    def load_plugin(self, name: str, app):
        if name in self.plugins:
            module = importlib.import_module(f"plugins.{name}")
            if hasattr(module, "register"):
                module.register(app)
                self.plugins[name] = module

plugin_manager = PluginManager()
plugin_manager.discover_plugins()

# Example API for plugin management
router = APIRouter()

@router.get("/plugins")
def list_plugins():
    return {"plugins": list(plugin_manager.plugins.keys())}

@router.post("/plugins/load/{plugin_name}")
def load_plugin(plugin_name: str, request: Request):
    from dashboard.main import app
    plugin_manager.load_plugin(plugin_name, app)
    return {"status": "loaded", "plugin": plugin_name}
