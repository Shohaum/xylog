from __future__ import annotations

from collections.abc import Iterable

from .context import bind, clear_context, get_context
from .exception_analyzer import (
    CompactException,
    ExceptionAnalyzer,
    ExceptionLocation,
)
from .filters import (
    Filter,
    FunctionFilter,
    LevelFilter,
    LoggerNameFilter,
)
from .formatter import (
    ColoredFormatter,
    DefaultFormatter,
    Formatter,
    JsonFormatter,
)
from .handlers import (
    AsyncHandler,
    ConsoleHandler,
    FileHandler,
    Handler,
    RotatingFileHandler,
)
from .levels import LogLevel
from .logger import Logger
from .manager import LoggerManager

_manager = LoggerManager()


def configure(
    *,
    level: LogLevel | None = None,
    handlers: Iterable[Handler] | None = None,
) -> None:
    _manager.configure(
        level=level,
        handlers=handlers,
    )


def get_logger(
    name: str,
    *,
    level: LogLevel | None = None,
    handlers: Iterable[Handler] | None = None,
    filters: Iterable[Filter] | None = None,
    propagate: bool = True,
) -> Logger:
    return _manager.get_logger(
        name,
        level=level,
        handlers=handlers,
        filters=filters,
        propagate=propagate,
    )


def shutdown() -> None:
    _manager.clear()


__all__ = [
    "Logger",
    "LoggerManager",
    "LogLevel",
    "get_logger",
    "configure",
    "shutdown",
    "Handler",
    "ConsoleHandler",
    "FileHandler",
    "RotatingFileHandler",
    "AsyncHandler",
    "Formatter",
    "DefaultFormatter",
    "JsonFormatter",
    "ColoredFormatter",
    "Filter",
    "LevelFilter",
    "LoggerNameFilter",
    "FunctionFilter",
    "bind",
    "clear_context",
    "get_context",
    "ExceptionAnalyzer",
    "ExceptionLocation",
    "CompactException",
]