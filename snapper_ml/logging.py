"""
This module is for logging utility functions.
"""
import logging
import os
import coloredlogs
from snapper_ml.config.models import Settings


logger = logging.getLogger(__name__)


def setup_logging(experiment_name, settings: Settings = Settings()):
    global logger
    logger = logging.getLogger(__name__)

    if not os.path.exists(settings.SNAPPER_ML_LOGS_FOLDER):
        os.mkdir(settings.SNAPPER_ML_LOGS_FOLDER)

    info_handler = logging.FileHandler(
        os.path.join(settings.SNAPPER_ML_LOGS_FOLDER, f'{experiment_name}.info.log'))
    error_handler = logging.FileHandler(
        os.path.join(settings.SNAPPER_ML_LOGS_FOLDER, f'{experiment_name}.error.log'))
    console = logging.StreamHandler()

    simple_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    descriptive_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    info_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    console.setLevel(logging.DEBUG)

    info_handler.setFormatter(logging.Formatter(descriptive_format))
    error_handler.setFormatter(logging.Formatter(descriptive_format))
    console.setFormatter(logging.Formatter(simple_format))

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console)

    coloredlogs.install(fmt=simple_format, level='DEBUG', logger=logger)
