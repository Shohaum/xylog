from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .exception_info import ExceptionInfo


@dataclass(frozen=True, slots=True)
class ExceptionLocation:
    filename: str
    line_number: int
    function_name: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "file": self.filename,
            "line": self.line_number,
            "function": self.function_name,
        }


@dataclass(frozen=True, slots=True)
class CompactException:
    exception_type: str
    message: str
    location: ExceptionLocation | None
    cause: CompactException | None = None
    context: CompactException | None = None
    children: tuple[CompactException, ...] = ()

    @property
    def is_group(self) -> bool:
        return bool(self.children)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "type": self.exception_type,
            "message": self.message,
            "location": (
                self.location.to_dict()
                if self.location is not None
                else None
            ),
        }

        if self.cause is not None:
            data["cause"] = self.cause.to_dict()

        if self.context is not None:
            data["context"] = self.context.to_dict()

        if self.children:
            data["children"] = [
                child.to_dict()
                for child in self.children
            ]

        return data


class ExceptionAnalyzer:
    __slots__ = ()

    def analyze(
        self,
        exception: ExceptionInfo,
    ) -> CompactException:
        if not isinstance(exception, ExceptionInfo):
            raise TypeError(
                "exception must be an ExceptionInfo"
            )

        return self._analyze(
            exception.traceback,
            active=set(),
        )

    def _analyze(
        self,
        traceback_exception: Any,
        *,
        active: set[int],
    ) -> CompactException:
        identity = id(traceback_exception)

        if identity in active:
            return CompactException(
                exception_type=self._exception_type(
                    traceback_exception
                ),
                message="<recursive exception reference>",
                location=None,
            )

        active.add(identity)

        try:
            cause = None

            if traceback_exception.__cause__ is not None:
                cause = self._analyze(
                    traceback_exception.__cause__,
                    active=active,
                )

            exceptions = getattr(
                traceback_exception,
                "exceptions",
                None,
            )

            children: tuple[CompactException, ...] = ()

            if exceptions:
                children = tuple(
                    self._analyze(
                        child,
                        active=active,
                    )
                    for child in exceptions
                )

            context = None

            if traceback_exception.__context__ is not None:
                context_exception = traceback_exception.__context__

                # If the context is already represented somewhere
                # inside the exception group's children, don't show
                # it again as a separate context chain.
                if not self._contains_equivalent(
                    exceptions or (),
                    context_exception,
                ):
                    context = self._analyze(
                        context_exception,
                        active=active,
                    )

            return CompactException(
                exception_type=self._exception_type(
                    traceback_exception
                ),
                message=self._message(
                    traceback_exception
                ),
                location=self._location(
                    traceback_exception
                ),
                cause=cause,
                context=context,
                children=children,
            )

        finally:
            active.remove(identity)

    @classmethod
    def _contains_equivalent(
        cls,
        exceptions: tuple[Any, ...] | list[Any],
        target: Any,
    ) -> bool:
        """
        Return True when target is already represented somewhere
        inside an exception group's child tree.

        TracebackException creates separate snapshot objects for
        the same underlying exception when that exception appears
        both as a group child and as __context__, so object identity
        cannot be used here.
        """

        for exception in exceptions:
            if cls._equivalent(exception, target):
                return True

            children = getattr(
                exception,
                "exceptions",
                None,
            )

            if children and cls._contains_equivalent(
                children,
                target,
            ):
                return True

        return False

    @classmethod
    def _equivalent(
        cls,
        first: Any,
        second: Any,
    ) -> bool:
        """
        Determine whether two TracebackException snapshots
        represent the same exception.
        """

        if cls._exception_type(first) != cls._exception_type(second):
            return False

        if cls._message(first) != cls._message(second):
            return False

        first_stack = cls._stack_signature(first)
        second_stack = cls._stack_signature(second)

        return first_stack == second_stack

    @staticmethod
    def _stack_signature(
        traceback_exception: Any,
    ) -> tuple[tuple[str, int, str], ...]:
        stack = traceback_exception.stack

        if not stack:
            return ()

        return tuple(
            (
                frame.filename,
                frame.lineno,
                frame.name,
            )
            for frame in stack
        )

    @staticmethod
    def _exception_type(
        traceback_exception: Any,
    ) -> str:
        exception_type = getattr(
            traceback_exception,
            "exc_type_str",
            None,
        )

        if exception_type:
            return exception_type

        exc_type = getattr(
            traceback_exception,
            "exc_type",
            None,
        )

        if exc_type is None:
            return "UnknownException"

        return getattr(
            exc_type,
            "__qualname__",
            getattr(
                exc_type,
                "__name__",
                str(exc_type),
            ),
        )

    @staticmethod
    def _message(
        traceback_exception: Any,
    ) -> str:
        message = getattr(
            traceback_exception,
            "_str",
            None,
        )

        if message is not None:
            message = str(message).strip()

            if traceback_exception.exceptions:
                message = re.sub(
                    r"\s+\(\d+ sub-exceptions?\)$",
                    "",
                    message,
                )

            return message

        formatted = "".join(
            traceback_exception.format_exception_only()
        ).strip()

        if not formatted:
            return ""

        first_line = formatted.splitlines()[0]

        exception_type = ExceptionAnalyzer._exception_type(
            traceback_exception
        )

        prefix = f"{exception_type}:"

        if first_line.startswith(prefix):
            return first_line[len(prefix):].strip()

        if first_line == exception_type:
            return ""

        return first_line

    @staticmethod
    def _location(
        traceback_exception: Any,
    ) -> ExceptionLocation | None:
        stack = traceback_exception.stack

        if not stack:
            return None

        frame = stack[-1]

        return ExceptionLocation(
            filename=frame.filename,
            line_number=frame.lineno,
            function_name=frame.name,
        )