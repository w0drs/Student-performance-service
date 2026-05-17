import logging
import logging.config
import json
from pathlib import Path


def setup_logging():
    """Настройка логирования"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    config_path = Path("logging.conf")

    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)

        logging.config.dictConfig(config)

    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s : %(name)s : %(levelname)s : %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/project.log")
            ]
        )

    logger = logging.getLogger(__name__)
    logger.info("Logging initialized successfully")
