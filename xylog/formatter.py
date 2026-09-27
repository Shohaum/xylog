from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import UTC, tzinfo
from typing import Any, Literal

from .exception_analyzer import CompactException, ExceptionAnalyzer
from .record import LogRecord


ExceptionMode = Literal["full", "compact", "none"]

_VALID_EXCEPTION_MODES = frozenset(
    {"full", "compact", "none"}
)


class Formatter(ABC):
    @abstractmethod
    def format(self, record: LogRecord, *, color: bool = False) -> str:
        raise NotImplementedError


class DefaultFormatter(Formatter):
    __slots__ = (
        "_timestamp_format",
        "_tzinfo",
        "_include_caller",
        "_exception_mode",
        "_exception_analyzer",
    )

    def __init__(
        self,
        *,
        timestamp_format: str = "%Y-%m-%d %H:%M:%S.%f %Z",
        tzinfo: tzinfo = UTC,
        include_caller: bool = True,
        exception_mode: ExceptionMode = "full",
    ) -> None:
        if exception_mode not in _VALID_EXCEPTION_MODES:
            raise ValueError(
                "exception_mode must be one of: "
                "'full', 'compact', 'none'"
            )

        self._timestamp_format = timestamp_format
        self._tzinfo = tzinfo
        self._include_caller = include_caller
        self._exception_mode = exception_mode
        self._exception_analyzer = ExceptionAnalyzer()

    @property
    def exception_mode(self) -> ExceptionMode:
        return self._exception_mode

    def format(self, record: LogRecord, *, color: bool = False) -> str:
        timestamp = record.timestamp.astimezone(
            self._tzinfo
        ).strftime(self._timestamp_format)

        parts = [
            timestamp,
            f"[{record.level.name}]",
            f"[{record.logger_name}]",
            record.message,
        ]

        if self._include_caller:
            parts.append(
                f"({record.caller.file_path}:{record.caller.line_number})"
            )

        if record.extra:
            parts.append(
                " ".join(
                    f"{key}={value!r}"
                    for key, value in record.extra.items()
                )
            )

        text = " ".join(parts)

        if record.exception is not None:
            exception_text = self._format_exception(
                record,
            )

            if exception_text:
                text = f"{text}\n{exception_text}"

        return text

    def _format_exception(self, record: LogRecord) -> str:
        exception = record.exception

        if exception is None:
            return ""

        if self._exception_mode == "none":
            return ""

        if self._exception_mode == "full":
            return exception.format().rstrip()

        compact = self._exception_analyzer.analyze(exception)

        return _format_compact_exception(compact)


class JsonFormatter(Formatter):
    __slots__ = (
        "_include_caller",
        "_exception_mode",
        "_exception_analyzer",
    )

    def __init__(
        self,
        *,
        include_caller: bool = True,
        exception_mode: ExceptionMode = "full",
    ) -> None:
        if exception_mode not in _VALID_EXCEPTION_MODES:
            raise ValueError(
                "exception_mode must be one of: "
                "'full', 'compact', 'none'"
            )

        self._include_caller = include_caller
        self._exception_mode = exception_mode
        self._exception_analyzer = ExceptionAnalyzer()

    @property
    def exception_mode(self) -> ExceptionMode:
        return self._exception_mode

    def format(self, record: LogRecord, *, color: bool = False) -> str:
        data: dict[str, Any] = {
            "timestamp": record.timestamp.isoformat(),
            "level": record.level.name,
            "logger": record.logger_name,
            "message": record.message,
            "process_id": record.process_id,
            "thread_id": record.thread_id,
            "extra": dict(record.extra),
        }

        if self._include_caller:
            data["caller"] = {
                "file": record.caller.file_path,
                "function": record.caller.function_name,
                "line": record.caller.line_number,
            }

        if record.exception is not None:
            self._add_exception(
                data,
                record,
            )

        return json.dumps(
            data,
            default=repr,
            ensure_ascii=False,
        )

    def _add_exception(
        self,
        data: dict[str, Any],
        record: LogRecord,
    ) -> None:
        exception = record.exception

        if exception is None:
            return

        if self._exception_mode == "none":
            return

        if self._exception_mode == "full":
            compact = self._exception_analyzer.analyze(exception)

            exception_data: dict[str, Any] = {
                "type": exception.exception_type,
                "message": exception.message,
                "traceback": exception.format(),
            }

            if compact.location is not None:
                exception_data["location"] = (
                    compact.location.to_dict()
                )

            data["exception"] = exception_data
            return

        compact = self._exception_analyzer.analyze(exception)

        data["exception"] = compact.to_dict()


class ColoredFormatter(DefaultFormatter):
    __slots__ = (
        "_colors",
        "_reset",
    )

    _RESET = "\033[0m"

    _DEFAULT_COLORS = {
        "TRACE": "\033[90m",
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }

    def __init__(
        self,
        *,
        timestamp_format: str = "%Y-%m-%d %H:%M:%S.%f %Z",
        tzinfo: tzinfo = UTC,
        include_caller: bool = True,
        colors: dict[str, str] | None = None,
        exception_mode: ExceptionMode = "full",
    ) -> None:
        super().__init__(
            timestamp_format=timestamp_format,
            tzinfo=tzinfo,
            include_caller=include_caller,
            exception_mode=exception_mode,
        )

        self._colors = (
            dict(colors)
            if colors is not None
            else self._DEFAULT_COLORS.copy()
        )

        self._reset = self._RESET

    def format(
        self,
        record: LogRecord,
        *,
        color: bool = False,
    ) -> str:
        message = super().format(
            record,
            color=False,
        )

        if not color:
            return message

        color_code = self._colors.get(
            record.level.name
        )

        if color_code is None:
            return message

        return f"{color_code}{message}{self._reset}"


def _format_compact_exception(
    exception: CompactException,
) -> str:
    lines: list[str] = []

    _append_exception(
        lines,
        exception,
        prefix="",
        connector=None,
    )

    return "\n".join(lines)


def _append_exception(
    lines: list[str],
    exception: CompactException,
    *,
    prefix: str,
    connector: str | None,
) -> None:
    location = _format_location(exception)

    header = (
        f"{exception.exception_type}: "
        f"{exception.message}"
    )

    if connector is None:
        lines.append(
            f"{prefix}{header}"
        )
    else:
        lines.append(
            f"{prefix}{connector} {header}"
        )

    if location:
        if connector == "├─":
            location_prefix = f"{prefix}│  "
        elif connector == "└─":
            location_prefix = f"{prefix}   "
        else:
            location_prefix = prefix

        lines.append(
            f"{location_prefix}→ {location}"
        )

    for index, child in enumerate(exception.children):
        is_last = index == len(exception.children) - 1

        child_connector = (
            "└─"
            if is_last
            else "├─"
        )

        child_prefix = prefix

        if connector is not None:
            child_prefix += (
                "   "
                if connector == "└─"
                else "│  "
            )

        _append_exception(
            lines,
            child,
            prefix=child_prefix,
            connector=child_connector,
        )

    # Python's traceback semantics give explicit __cause__
    # precedence over implicit __context__.
    if exception.cause is not None:
        lines.append("")
        lines.append(
            f"{prefix}Caused by:"
        )

        _append_exception(
            lines,
            exception.cause,
            prefix=f"{prefix}  ",
            connector=None,
        )

    elif exception.context is not None:
        lines.append("")
        lines.append(
            f"{prefix}During handling of the above exception:"
        )

        _append_exception(
            lines,
            exception.context,
            prefix=f"{prefix}  ",
            connector=None,
        )


def _format_location(
    exception: CompactException,
) -> str:
    if exception.location is None:
        return ""

    location = exception.location

    return (
        f"{location.filename}:"
        f"{location.line_number} "
        f"in {location.function_name}"
    )