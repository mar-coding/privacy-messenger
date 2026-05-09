import logging
import sys
from collections.abc import MutableMapping
from typing import Any

from app.settings import settings


class _ColorFormatter(logging.Formatter):
    """Console formatter with per-level ANSI colors. Colors are disabled
    automatically when stdout is not a TTY (files, pipes, Docker, journald)."""

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    _FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    _LEVEL_COLOR = {
        logging.DEBUG: GREY,
        logging.INFO: GREY,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED,
    }

    def __init__(self, *, use_color: bool) -> None:
        super().__init__(self._FMT)
        if use_color:
            self._formatters = {
                level: logging.Formatter(f"{color}{self._FMT}{self.RESET}")
                for level, color in self._LEVEL_COLOR.items()
            }
        else:
            plain = logging.Formatter(self._FMT)
            self._formatters = dict.fromkeys(self._LEVEL_COLOR, plain)

    def format(self, record: logging.LogRecord) -> str:
        formatter = self._formatters.get(record.levelno)
        if formatter is None:
            return super().format(record)
        return formatter.format(record)


def configure_logging() -> None:
    """Configure the root logger. Call once at application startup, before
    creating the FastAPI app, so import-time logs use the configured handlers."""

    level = logging.DEBUG if settings.DEBUG_MODE else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_ColorFormatter(use_color=sys.stdout.isatty()))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # Align uvicorn with our handlers; silence access logs unless explicitly wanted.
    for name in ("uvicorn", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


class ContextLogger(logging.LoggerAdapter[logging.Logger]):
    """LoggerAdapter that appends a `key=value` context block to each message.

    For request-scoped context (request id, user id), prefer a `logging.Filter`
    backed by `contextvars` or `structlog` — this adapter must be threaded
    through every call site, which is rarely worth it."""

    def __init__(
        self, logger: logging.Logger, extra: dict[str, Any] | None = None
    ) -> None:
        super().__init__(logger, extra or {})

    def process(
        self, msg: str, kwargs: MutableMapping[str, Any]
    ) -> tuple[str, MutableMapping[str, Any]]:
        if self.extra:
            ctx = " ".join(f"{k}={v}" for k, v in self.extra.items())
            msg = f"{msg} [{ctx}]"
        return msg, kwargs
