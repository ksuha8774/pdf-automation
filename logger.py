import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'details'):
            log_entry["details"] = record.details
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logger(name: str = "pdf_script") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler("script_log.json", maxBytes=5_000_000, backupCount=5)
    handler.setFormatter(JsonFormatter())
    
    logger.addHandler(handler)
    return logger