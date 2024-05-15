"""PyWorkbench client in Python: ansys-workbench-core."""

__all__ = ["__version__"]

"""Version of ansys-workbench-core module."""
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

# Read from the pyproject.toml
__version__ = importlib_metadata.version("ansys-workbench-core")

# exposed API
from ansys.workbench.core.launch_workbench import launch_workbench, connect_workbench
