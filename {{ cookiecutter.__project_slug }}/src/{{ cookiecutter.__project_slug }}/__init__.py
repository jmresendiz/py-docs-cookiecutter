# read version from installed package
from importlib.metadata import version

__version__ = version("{{ cookiecutter.__project_slug }}")
