import logging

from app.config import get_settings

_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def setup_logging() -> None:
    level = getattr(logging, get_settings().log_level.upper(), logging.INFO)
    logging.basicConfig(level=level, format=_FORMAT)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
