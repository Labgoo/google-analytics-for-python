__author__ = 'minhtule'


import logging

GA_LOGGING_LEVEL = logging.DEBUG


def init_ga_logger():
    formatter = logging.Formatter("%(levelname)-8s %(asctime)s \t %(filename)s:%(lineno)d [Google Analytics] %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger("google_analytics")
    logger.setLevel(GA_LOGGING_LEVEL)
    logger.addHandler(handler)
    return logger

ga_logger = init_ga_logger()


def is_empty_string(text):
    return not text.strip()