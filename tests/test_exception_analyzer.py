from __future__ import annotations

import json

import pytest

from xylog.exception_analyzer import (
    CompactException,
    ExceptionAnalyzer,
)
from xylog.exception_info import ExceptionInfo
from xylog.formatter import DefaultFormatter, JsonFormatter


def _capture_exception_info(func) -> ExceptionInfo:
    try:
        func()
    except BaseException as exc:
        return ExceptionInfo.from_exception(exc)

    raise AssertionError("Expected an exception")


def _raise_value_error() -> None:
    raise ValueError("Invalid user ID")


def test_analyzes_normal_exception() -> None:
    info = _capture_exception_info(
        _raise_value_error
    )

    result = ExceptionAnalyzer().analyze(info)

    assert isinstance(result, CompactException)
    assert result.exception_type == "ValueError"
    assert result.message == "Invalid user ID"
    assert result.location is not None
    assert result.location.function_name == "_raise_value_error"
    assert result.location.line_number > 0
    assert result.cause is None
    assert result.context is None
    assert result.children == ()


def test_analyzes_explicit_cause() -> None:
    def raise_error() -> None:
        try:
            raise ConnectionError("connection refused")
        except ConnectionError as exc:
            raise RuntimeError("Unable to load user") from exc

    info = _capture_exception_info(raise_error)

    result = ExceptionAnalyzer().analyze(info)

    assert result.exception_type == "RuntimeError"
    assert result.message == "Unable to load user"

    assert result.cause is not None
    assert result.cause.exception_type == "ConnectionError"
    assert result.cause.message == "connection refused"

    assert result.context is None


def test_analyzes_implicit_context() -> None:
    def raise_error() -> None:
        try:
            raise ValueError("invalid value")
        except ValueError:
            raise RuntimeError("operation failed")

    info = _capture_exception_info(raise_error)

    result = ExceptionAnalyzer().analyze(info)

    assert result.exception_type == "RuntimeError"
    assert result.message == "operation failed"

    assert result.cause is None
    assert result.context is not None

    assert result.context.exception_type == "ValueError"
    assert result.context.message == "invalid value"


@pytest.mark.skipif(
    not hasattr(__builtins__, "ExceptionGroup"),
    reason="ExceptionGroup requires Python 3.11+",
)
def test_analyzes_exception_group() -> None:
    def raise_group() -> None:
        raise ExceptionGroup(
            "Multiple operations failed",
            [
                ValueError("Invalid user"),
                TimeoutError("Database timed out"),
            ],
        )

    info = _capture_exception_info(raise_group)

    result = ExceptionAnalyzer().analyze(info)

    assert result.exception_type == "ExceptionGroup"
    assert result.message == "Multiple operations failed"

    assert len(result.children) == 2

    assert result.children[0].exception_type == "ValueError"
    assert result.children[0].message == "Invalid user"

    assert result.children[1].exception_type == "TimeoutError"
    assert result.children[1].message == "Database timed out"


def test_analyzes_nested_exception_group() -> None:
    def raise_group() -> None:
        raise ExceptionGroup(
            "outer",
            [
                ExceptionGroup(
                    "inner",
                    [
                        ValueError("invalid"),
                        TypeError("wrong type"),
                    ],
                ),
                TimeoutError("timeout"),
            ],
        )

    info = _capture_exception_info(raise_group)

    result = ExceptionAnalyzer().analyze(info)

    assert result.exception_type == "ExceptionGroup"
    assert result.message == "outer"

    assert len(result.children) == 2

    inner = result.children[0]

    assert inner.exception_type == "ExceptionGroup"
    assert inner.message == "inner"

    assert len(inner.children) == 2
    assert inner.children[0].exception_type == "ValueError"
    assert inner.children[1].exception_type == "TypeError"

    assert result.children[1].exception_type == "TimeoutError"


def test_compact_exception_to_dict() -> None:
    def raise_error() -> None:
        raise ValueError("bad value")

    info = _capture_exception_info(raise_error)

    result = ExceptionAnalyzer().analyze(info)
    data = result.to_dict()

    assert data["type"] == "ValueError"
    assert data["message"] == "bad value"

    assert data["location"]["file"]
    assert data["location"]["line"] > 0
    assert data["location"]["function"] == "raise_error"


def test_default_formatter_compact_exception() -> None:
    def raise_error() -> None:
        raise ValueError("Invalid user ID")

    info = _capture_exception_info(raise_error)

    from xylog import LogLevel
    from xylog.record import LogRecord
    from xylog.caller_info import CallerInfo

    record = LogRecord(
        timestamp=__import__("datetime").datetime.now(
            __import__("datetime").UTC
        ),
        level=LogLevel.ERROR,
        logger_name="users",
        message="Failed to validate user",
        process_id=1,
        thread_id=1,
        caller=CallerInfo(
            file_path="test.py",
            function_name="test",
            line_number=1,
        ),
        exception=info,
        extra={},
    )

    formatter = DefaultFormatter(
        exception_mode="compact"
    )

    output = formatter.format(record)

    assert "ValueError: Invalid user ID" in output
    assert "raise_error" in output
    assert "→" in output

    assert "Traceback (most recent call last)" not in output


def test_default_formatter_none_exception() -> None:
    def raise_error() -> None:
        raise ValueError("secret")

    info = _capture_exception_info(raise_error)

    from xylog import LogLevel
    from xylog.record import LogRecord
    from xylog.caller_info import CallerInfo
    from datetime import UTC, datetime

    record = LogRecord(
        timestamp=datetime.now(UTC),
        level=LogLevel.ERROR,
        logger_name="users",
        message="Failed",
        process_id=1,
        thread_id=1,
        caller=CallerInfo(
            file_path="test.py",
            function_name="test",
            line_number=1,
        ),
        exception=info,
        extra={},
    )

    formatter = DefaultFormatter(
        exception_mode="none"
    )

    output = formatter.format(record)

    assert "ValueError" not in output
    assert "Traceback" not in output


def test_json_formatter_compact_exception() -> None:
    def raise_error() -> None:
        raise ValueError("Invalid user")

    info = _capture_exception_info(raise_error)

    from datetime import UTC, datetime

    from xylog import LogLevel
    from xylog.caller_info import CallerInfo
    from xylog.record import LogRecord

    record = LogRecord(
        timestamp=datetime.now(UTC),
        level=LogLevel.ERROR,
        logger_name="users",
        message="Failed",
        process_id=1,
        thread_id=1,
        caller=CallerInfo(
            file_path="test.py",
            function_name="test",
            line_number=1,
        ),
        exception=info,
        extra={},
    )

    formatter = JsonFormatter(
        exception_mode="compact"
    )

    output = formatter.format(record)
    data = json.loads(output)

    assert data["exception"]["type"] == "ValueError"
    assert data["exception"]["message"] == "Invalid user"

    assert data["exception"]["location"]["function"] == (
        "raise_error"
    )

    assert "traceback" not in data["exception"]


def test_json_formatter_full_preserves_traceback() -> None:
    def raise_error() -> None:
        raise ValueError("Invalid user")

    info = _capture_exception_info(raise_error)

    from datetime import UTC, datetime

    from xylog import LogLevel
    from xylog.caller_info import CallerInfo
    from xylog.record import LogRecord

    record = LogRecord(
        timestamp=datetime.now(UTC),
        level=LogLevel.ERROR,
        logger_name="users",
        message="Failed",
        process_id=1,
        thread_id=1,
        caller=CallerInfo(
            file_path="test.py",
            function_name="test",
            line_number=1,
        ),
        exception=info,
        extra={},
    )

    formatter = JsonFormatter(
        exception_mode="full"
    )

    output = formatter.format(record)
    data = json.loads(output)

    assert data["exception"]["type"] == "ValueError"
    assert data["exception"]["message"] == "ValueError: Invalid user"
    assert "Traceback" in data["exception"]["traceback"]

    assert data["exception"]["location"]["function"] == (
        "raise_error"
    )

def test_exception_group_does_not_duplicate_context_child() -> None:
    def raise_group() -> None:
        validation_group = ExceptionGroup(
            "Validation failed",
            [
                ValueError("Invalid user"),
                PermissionError("Insufficient permissions"),
            ],
        )

        try:
            raise TimeoutError("Database timed out")
        except TimeoutError as exc:
            raise ExceptionGroup(
                "Processing failed",
                [
                    validation_group,
                    exc,
                ],
            )

    info = _capture_exception_info(raise_group)

    result = ExceptionAnalyzer().analyze(info)

    assert result.exception_type == "ExceptionGroup"
    assert result.message == "Processing failed"

    assert result.context is None

    assert len(result.children) == 2

    validation = result.children[0]

    assert validation.exception_type == "ExceptionGroup"
    assert validation.message == "Validation failed"
    assert validation.context is None

    assert len(validation.children) == 2
    assert validation.children[0].exception_type == "ValueError"
    assert validation.children[0].message == "Invalid user"
    assert validation.children[1].exception_type == "PermissionError"
    assert validation.children[1].message == "Insufficient permissions"

    timeout = result.children[1]

    assert timeout.exception_type == "TimeoutError"
    assert timeout.message == "Database timed out"

def test_exception_group_without_own_traceback_has_no_location() -> None:
    def raise_group() -> None:
        inner = ExceptionGroup(
            "Validation failed",
            [
                ValueError("Invalid user"),
            ],
        )

        raise ExceptionGroup(
            "Processing failed",
            [inner],
        )

    info = _capture_exception_info(raise_group)

    result = ExceptionAnalyzer().analyze(info)

    assert result.exception_type == "ExceptionGroup"
    assert result.message == "Processing failed"
    assert result.location is not None

    inner = result.children[0]

    assert inner.exception_type == "ExceptionGroup"
    assert inner.message == "Validation failed"
    assert inner.location is None

    assert len(inner.children) == 1
    assert inner.children[0].exception_type == "ValueError"