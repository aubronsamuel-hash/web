import json
import logging
import logging.config
from typing import Any, Dict

from .settings import get_settings

REQUEST_ID_ATTR = "request_id"


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, REQUEST_ID_ATTR):
            setattr(record, REQUEST_ID_ATTR, "-")
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data: Dict[str, Any] = {
            "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
            "request_id": getattr(record, REQUEST_ID_ATTR, "-"),
        }
        # Ajout contextuel commun si disponible
        for k in ("path", "method", "status_code"):
            if hasattr(record, k):
                data[k] = getattr(record, k)
        return json.dumps(data, separators=(",", ":"))


def configure_logging() -> None:
    level = get_settings().log_level.upper()
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {"()": RequestIdFilter},
        },
        "formatters": {
            "json": {"()": JsonFormatter},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "filters": ["request_id"],
                "formatter": "json",
                "level": level,
            }
        },
        "loggers": {
            "uvicorn": {"handlers": ["console"], "level": level, "propagate": False},
            "uvicorn.error": {"handlers": ["console"], "level": level, "propagate": False},
            "uvicorn.access": {"handlers": ["console"], "level": level, "propagate": False},
            "app": {"handlers": ["console"], "level": level, "propagate": False},
        },
        "root": {"handlers": ["console"], "level": level},
    }
    logging.config.dictConfig(cfg)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
