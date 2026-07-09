"""
Logging system.
"""

import logging

from logging.handlers import RotatingFileHandler


import config


def initialise_logger():

    config.LOG_FOLDER.mkdir(exist_ok=True)

    logfile = config.LOG_FOLDER / "music_collection.log"

    logger = logging.getLogger()

    logger.setLevel(config.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        logfile,
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    logger.info("===================================")
    logger.info("Music Collection Manager started.")
    logger.info("===================================")

    return logger