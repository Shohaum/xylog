# Logger interface
# from xylog import get_logger

# logger = get_logger("Demo")

# logger.info("Application started")

# logger.debug("Debug message")

# logger.warning("Low disk space")

# logger.error("Something went wrong")

# Exception Catching
# try:
#     10 / 0
# except Exception as exc:
#     logger.exception(
#         "Division failed",
#         exception=exc,
#     )

# Logger Cache
# from xylog import get_logger

# logger1 = get_logger("Auth")
# logger2 = get_logger("Auth")

# print(logger1 is logger2)

# Different Loggers
# logger1 = get_logger("Auth")
# logger2 = get_logger("Database")

# print(logger1 is logger2)

# Log Level Filtering
# from xylog import get_logger
# from xylog.levels import LogLevel

# logger = get_logger("Demo")

# logger.level = LogLevel.ERROR

# logger.info("Hidden")

# logger.warning("Hidden")

# logger.error("Visible")

# File Handler
# from xylog import get_logger
# from xylog.handlers import FileHandler

# logger = get_logger("FileLogger")

# logger.add_handler(
#     FileHandler("logs/app.log")
# )

# logger.info("Written to file")

# # Extra Metadata
# logger.info(
#     "User logged in",
#     extra={
#         "user_id": 42,
#         "country": "India",
#     },
# )

# Thread Safety
# import threading

# from xylog import get_logger

# logger = get_logger("Threads")


# def worker(index: int):
#     for i in range(100):
#         logger.info(f"Worker {index}: {i}")


# threads = [
#     threading.Thread(target=worker, args=(i,))
#     for i in range(10)
# ]

# for t in threads:
#     t.start()

# for t in threads:
#     t.join()

# Multiple Handlers
# from xylog import get_logger
# from xylog.handlers import FileHandler

# logger = get_logger("Demo")

# logger.add_handler(
#     FileHandler("logs/demo.log")
# )

# logger.info("Hello")

# Json logging
# from xylog import get_logger
# from xylog.formatter import JsonFormatter
# from xylog.handlers import ConsoleHandler

# logger = get_logger(
#     "API",
#     handlers=[
#         ConsoleHandler(
#             formatter=JsonFormatter()
#         )
#     ],
# )

# with logger.context(
#     request_id="req-123",
#     user_id=42,
# ):
#     logger.info("Request started")

# Async logging
# from xylog import get_logger
# from xylog.handlers import AsyncHandler, FileHandler

# handler = AsyncHandler(
#     FileHandler("logs/async.log")
# )

# logger = get_logger(
#     "AsyncTest",
#     handlers=[handler],
# )

# for i in range(1000):
#     logger.info(f"Message {i}")

# logger.close()

# Rotating file handling
# from xylog import get_logger
# from xylog.handlers import RotatingFileHandler

# handler = RotatingFileHandler(
#     "logs/rotation.log",
#     max_bytes=500,
#     backup_count=3,
# )

# logger = get_logger(
#     "RotationTest",
#     handlers=[handler],
# )

# for i in range(100):
#     logger.info(
#         f"This is test message number {i}"
#     )

# logger.close()

# Color output in the terminal
# from xylog import get_logger
# from xylog.formatter import ColoredFormatter
# from xylog.handlers import ConsoleHandler

# logger = get_logger(
#     "API",
#     handlers=[
#         ConsoleHandler(
#             formatter=ColoredFormatter()
#         )
#     ],
# )

# logger.debug("Debug information")
# logger.info("Server started")
# logger.warning("Cache miss")
# logger.error("Database timeout")
# logger.critical("System failure")

# Integration testing
# from xylog import get_logger
# from xylog.formatter import JsonFormatter
# from xylog.handlers import AsyncHandler, RotatingFileHandler

# handler = AsyncHandler(
#     RotatingFileHandler(
#         "logs/integration.log",
#         max_bytes=5_000,
#         backup_count=3,
#         formatter=JsonFormatter(),
#     )
# )

# logger = get_logger(
#     "IntegrationTest",
#     handlers=[handler],
# )

# with logger.context(
#     request_id="req-123",
#     user_id=42,
# ):
#     for i in range(1_000):
#         logger.info(
#             "Processing request",
#             extra={"iteration": i},
#         )

# logger.close()

# TTY test
# from xylog import get_logger
# from xylog.formatter import ColoredFormatter
# from xylog.handlers import ConsoleHandler

# logger = get_logger(
#     "TTYTest",
#     handlers=[
#         ConsoleHandler(
#             formatter=ColoredFormatter()
#         )
#     ],
# )

# logger.debug("Debug message")
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.critical("Critical message")

# Color formatter with file handler
# from xylog import get_logger
# from xylog.formatter import ColoredFormatter
# from xylog.handlers import FileHandler

# logger = get_logger(
#     "FileTest",
#     handlers=[
#         FileHandler(
#             "logs/color_test.log",
#             formatter=ColoredFormatter(),
#         )
#     ],
# )

# logger.info("This should not contain ANSI colors")

# logger.close()

# TTY detection with async handler
# from xylog import get_logger
# from xylog.formatter import ColoredFormatter
# from xylog.handlers import AsyncHandler, ConsoleHandler

# logger = get_logger(
#     "AsyncTTY",
#     handlers=[
#         AsyncHandler(
#             ConsoleHandler(
#                 formatter=ColoredFormatter()
#             )
#         )
#     ],
# )

# for i in range(100):
#     logger.info(f"Message {i}")

# logger.close()

# Logger filter
# from xylog import get_logger
# from xylog.filters import LevelFilter
# from xylog.levels import LogLevel

# logger = get_logger(
#     "FilterTest",
#     level=LogLevel.DEBUG,
#     filters=[
#         LevelFilter(LogLevel.ERROR),
#     ],
# )

# logger.debug("Should NOT appear")
# logger.info("Should NOT appear")
# logger.warning("Should NOT appear")
# logger.error("Should appear")
# logger.critical("Should appear")

# logger.close()

# Logger filter with different handlers
# from xylog import get_logger
# from xylog.filters import LevelFilter
# from xylog.handlers import ConsoleHandler, FileHandler
# from xylog.levels import LogLevel

# console = ConsoleHandler()

# file_handler = FileHandler(
#     "logs/errors.log",
#     filters=[
#         LevelFilter(LogLevel.ERROR),
#     ],
# )

# logger = get_logger(
#     "HandlerFilterTest",
#     handlers=[
#         console,
#         file_handler,
#     ],
# )

# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")

# logger.close()

# Logger filter with async
# from xylog import get_logger
# from xylog.filters import LevelFilter
# from xylog.handlers import AsyncHandler, FileHandler
# from xylog.levels import LogLevel

# handler = AsyncHandler(
#     FileHandler(
#         "logs/async-errors.log",
#     ),
#     filters=[
#         LevelFilter(LogLevel.ERROR),
#     ],
# )

# logger = get_logger(
#     "AsyncFilter",
#     handlers=[handler],
# )

# for i in range(100):
#     logger.info(f"Info {i}")

# for i in range(100):
#     logger.error(f"Error {i}")

# logger.close()

# Basic hierarchy
# from xylog import get_logger
# from xylog.levels import LogLevel

# app = get_logger("app")
# api = get_logger("app.api")
# auth = get_logger("app.api.auth")

# assert api.parent is app
# assert auth.parent is api

# print("Basic hierarchy passed")

# Level inheritence
# from xylog import get_logger
# from xylog.levels import LogLevel

# app = get_logger("app")
# api = get_logger("app.api")
# auth = get_logger("app.api.auth")
# app.level = LogLevel.WARNING

# assert api.level is None
# assert api.effective_level == LogLevel.WARNING

# assert auth.level is None
# assert auth.effective_level == LogLevel.WARNING

# print("Level inheritance passed")

# Child override
# from xylog import get_logger
# from xylog.levels import LogLevel

# app = get_logger("app")
# api = get_logger("app.api")
# auth = get_logger("app.api.auth")

# app.level = LogLevel.WARNING
# auth.level = LogLevel.DEBUG

# assert auth.effective_level == LogLevel.DEBUG
# assert api.effective_level == LogLevel.WARNING

# print("Child level override passed")

# Propagation test
# from pathlib import Path

# from xylog import get_logger
# from xylog.handlers import FileHandler

# log_path = Path("logs/hierarchy.log")

# if log_path.exists():
#     log_path.unlink()

# app = get_logger(
#     "application",
#     handlers=[
#         FileHandler(log_path)
#     ],
# )

# auth = get_logger("application.api.auth")

# auth.error("Authentication failed")

# app.close()
# auth.close()

# content = log_path.read_text()

# assert "Authentication failed" in content

# print("Propagation passed")

# Propagation disabled
# from pathlib import Path

# from xylog import get_logger
# from xylog.handlers import FileHandler

# log_path = Path("logs/no_propagation.log")

# if log_path.exists():
#     log_path.unlink()

# app = get_logger(
#     "service",
#     handlers=[
#         FileHandler(log_path)
#     ],
# )

# worker = get_logger(
#     "service.worker",
#     propagate=False,
# )

# worker.error("Worker failure")

# app.close()
# worker.close()

# content = (
#     log_path.read_text()
#     if log_path.exists()
#     else ""
# )

# assert "Worker failure" not in content

# print("Propagation disabled passed")

# Parent created AFTER child
# from xylog import get_logger

# child = get_logger("backend.api.auth")

# assert child.parent.name == ""

# parent = get_logger("backend.api")

# assert child.parent is parent

# print("Late parent creation passed")

# No duplicate logging
# from xylog import get_logger
# from xylog.handlers import FileHandler

# root = get_logger(
#     "myapp",
#     handlers=[
#         FileHandler("logs/duplicate.log")
#     ],
# )

# child = get_logger("myapp.api")

# child.error("ONE MESSAGE")

# root.close()
# child.close()

# Full hierarchy
# from xylog import get_logger

# root = get_logger("myapp")
# api = get_logger("myapp.api")
# auth = get_logger("myapp.api.auth")
# payments = get_logger("myapp.api.payments")
# worker = get_logger("myapp.worker")

# assert api.parent is root
# assert auth.parent is api
# assert payments.parent is api
# assert worker.parent is root

# print("Full hierarchy passed")

# Global level configuration
# from xylog import configure, get_logger
# from xylog.levels import LogLevel


# configure(
#     level=LogLevel.WARNING,
# )

# logger = get_logger("app.api")

# assert logger.effective_level == LogLevel.WARNING

# logger.info("Should NOT appear")
# logger.warning("Should appear")
# logger.error("Should appear")

# Global handlers
# from pathlib import Path

# from xylog import configure, get_logger
# from xylog.handlers import FileHandler

# path = Path("logs/config.log")

# if path.exists():
#     path.unlink()

# configure(
#     handlers=[
#         FileHandler(path),
#     ],
# )

# logger = get_logger("app.api.auth")

# logger.info("Configuration works")

# logger.close()

# assert "Configuration works" in path.read_text()

# Child override
# from xylog import configure, get_logger
# from xylog.levels import LogLevel

# configure(
#     level=LogLevel.WARNING,
# )

# logger = get_logger(
#     "app.debug",
#     level=LogLevel.DEBUG,
# )

# assert logger.effective_level == LogLevel.DEBUG

# Reconfiguration
# from xylog import configure, get_logger
# from xylog.levels import LogLevel
# configure(
#     level=LogLevel.ERROR,
# )

# logger = get_logger("app.api")

# assert logger.effective_level == LogLevel.ERROR

# configure(
#     level=LogLevel.DEBUG,
# )

# assert logger.effective_level == LogLevel.DEBUG

# Shutdown
# from xylog import shutdown

# shutdown()

# Nested context
# from xylog import get_logger

# logger = get_logger("ContextTest")

# with logger.context(request_id="req-123"):
#     logger.info("First")

#     with logger.context(user_id=42):
#         logger.info("Second")

#     logger.info("Third")

# logger.close()

# Explicit extra overrides context
# from xylog import get_logger

# logger = get_logger("ContextTest")
# with logger.context(user_id=42):
#     logger.info(
#         "Test",
#         extra={"user_id": 100},
#     )

# Temporarily clear context
# from xylog import clear_context
# from xylog import get_logger

# logger = get_logger("ContextTest")
# with logger.context(request_id="req-123"):
#     logger.info("Has context")

#     with clear_context():
#         logger.info("No context")

#     logger.info("Context restored")

# Async context capture
# from xylog import get_logger
# from xylog.handlers import AsyncHandler, FileHandler

# handler = AsyncHandler(
#     FileHandler("logs/context_async.log")
# )

# logger = get_logger(
#     "AsyncContext",
#     handlers=[handler],
# )

# with logger.context(request_id="req-123"):
#     logger.info("Message from request")

# logger.close()

# Full exception
# from xylog import get_logger

# logger = get_logger("app")

# def validate_user(user_id: int) -> None:
#     if user_id <= 0:
#         raise ValueError("Invalid user ID")

# def get_user(user_id: int) -> None:
#     validate_user(user_id)

# try:
#     get_user(-10)
# except Exception:
#     logger.exception("Failed to process user")

# Compact exception
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# formatter = DefaultFormatter(
#     exception_mode="compact",
# )

# handler = ConsoleHandler(
#     formatter=formatter,
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False
# )

# def validate_user(user_id: int) -> None:
#     if user_id <= 0:
#         raise ValueError("Invalid user ID")

# def get_user(user_id: int) -> None:
#     validate_user(user_id)

# try:
#     get_user(-10)
# except Exception:
#     logger.exception("Failed to process user")

# Explicit raise ... from ...
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# handler = ConsoleHandler(
#     formatter=DefaultFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def connect_database() -> None:
#     raise ConnectionError("connection refused")


# def load_user() -> None:
#     try:
#         connect_database()
#     except ConnectionError as exc:
#         raise RuntimeError("Unable to load user") from exc

# try:
#     load_user()
# except Exception:
#     logger.exception("Request failed")

# Implicit exception context
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# handler = ConsoleHandler(
#     formatter=DefaultFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def parse_user() -> None:
#     raise ValueError("Invalid user data")

# def process_user() -> None:
#     try:
#         parse_user()
#     except ValueError:
#         raise RuntimeError("Could not process user")

# try:
#     process_user()
# except Exception:
#     logger.exception("Request failed")

# ExceptionGroup
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# handler = ConsoleHandler(
#     formatter=DefaultFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def validate_user() -> None:
#     raise ValueError("Invalid user")

# def fetch_database() -> None:
#     raise TimeoutError("Database timed out")

# def process() -> None:
#     errors = []

#     try:
#         validate_user()
#     except Exception as exc:
#         errors.append(exc)

#     try:
#         fetch_database()
#     except Exception as exc:
#         errors.append(exc)

#     raise ExceptionGroup(
#         "Multiple operations failed",
#         errors,
#     )

# try:
#     process()
# except Exception:
#     logger.exception("Processing failed")

# Nested ExceptionGroup
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# handler = ConsoleHandler(
#     formatter=DefaultFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def validate_user() -> None:
#     raise ValueError("Invalid user")

# def validate_permissions() -> None:
#     raise PermissionError("Insufficient permissions")

# def database_operation() -> None:
#     raise TimeoutError("Database timed out")

# def process() -> None:
#     validation_errors = []

#     try:
#         validate_user()
#     except Exception as exc:
#         validation_errors.append(exc)

#     try:
#         validate_permissions()
#     except Exception as exc:
#         validation_errors.append(exc)

#     validation_group = ExceptionGroup(
#         "Validation failed",
#         validation_errors,
#     )

#     try:
#         database_operation()
#     except Exception as exc:
#         raise ExceptionGroup(
#             "Processing failed",
#             [
#                 validation_group,
#                 exc,
#             ],
#         )

# try:
#     process()
# except Exception:
#     logger.exception("Request failed")

# Test BaseExceptionGroup
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# handler = ConsoleHandler(
#     formatter=DefaultFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def operation_one() -> None:
#     raise ValueError("Operation one failed")

# def operation_two() -> None:
#     raise KeyboardInterrupt()

# try:
#     errors = []

#     try:
#         operation_one()
#     except BaseException as exc:
#         errors.append(exc)

#     try:
#         operation_two()
#     except BaseException as exc:
#         errors.append(exc)

#     raise BaseExceptionGroup(
#         "Operations failed",
#         errors,
#     )

# except BaseException:
#     logger.exception("Batch operation failed")

# # exception_mode="none"
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import DefaultFormatter

# handler = ConsoleHandler(
#     formatter=DefaultFormatter(
#         exception_mode="none",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def validate_user() -> None:
#     raise ValueError("Invalid user")

# try:
#     validate_user()
# except Exception:
#     logger.exception("Validation failed")

# # JSON compact
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import JsonFormatter

# handler = ConsoleHandler(
#     formatter=JsonFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def connect_database() -> None:
#     raise ConnectionError("connection refused")

# def load_user() -> None:
#     try:
#         connect_database()
#     except ConnectionError as exc:
#         raise RuntimeError("Unable to load user") from exc

# try:
#     load_user()
# except Exception:
#     logger.exception("Request failed")

# JSON + ExceptionGroup
# from xylog import get_logger
# from xylog.handlers import ConsoleHandler
# from xylog.formatter import JsonFormatter

# handler = ConsoleHandler(
#     formatter=JsonFormatter(
#         exception_mode="compact",
#     ),
# )

# logger = get_logger(
#     "app",
#     handlers=[handler],
#     propagate=False,
# )

# def validate_user() -> None:
#     raise ValueError("Invalid user")

# def validate_permissions() -> None:
#     raise PermissionError("Insufficient permissions")

# def database_operation() -> None:
#     raise TimeoutError("Database timed out")

# def process() -> None:
#     validation_errors = []

#     try:
#         validate_user()
#     except Exception as exc:
#         validation_errors.append(exc)

#     try:
#         validate_permissions()
#     except Exception as exc:
#         validation_errors.append(exc)

#     validation_group = ExceptionGroup(
#         "Validation failed",
#         validation_errors,
#     )

#     try:
#         database_operation()
#     except Exception as exc:
#         raise ExceptionGroup(
#             "Processing failed",
#             [
#                 validation_group,
#                 exc,
#             ],
#         )

# try:
#     process()
# except Exception:
#     logger.exception("Request failed")