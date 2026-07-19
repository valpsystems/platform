from __future__ import annotations

import sys

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    json_format = (
        '{{"timestamp":"{time:YYYY-MM-DD HH:mm:ss.SSS}",'
        '"level":"{level}",'
        '"module":"{name}",'
        '"function":"{function}",'
        '"line":{line},'
        '"message":"{message}"}}'
    )

    log_level = settings.LOG_LEVEL.upper()
    use_json = settings.LOG_FORMAT == "json"
    fmt = json_format if use_json else log_format

    # Console
    logger.add(
        sys.stdout,
        format=fmt,
        level=log_level,
        colorize=not use_json,
        backtrace=True,
        diagnose=settings.is_development,
    )

    # Application log
    logger.add(
        settings.LOGS_DIR / "app.log",
        format=fmt,
        level=log_level,
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=settings.is_development,
    )

    # Error log
    logger.add(
        settings.LOGS_DIR / "error.log",
        format=fmt,
        level="ERROR",
        rotation="100 MB",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    # Access log
    logger.add(
        settings.LOGS_DIR / "access.log",
        format=fmt,
        level="INFO",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        filter=lambda record: record["extra"].get("type") == "access",
    )


app_logger = logger.bind(type="app")
access_logger = logger.bind(type="access")
error_logger = logger.bind(type="error")
audit_logger = logger.bind(type="audit")
