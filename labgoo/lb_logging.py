__author__ = 'minhtule'

import logging

lb_logging_level = logging.DEBUG

# Create Labgoo logger
formatter = logging.Formatter("%(levelname)s %(asctime)s \t %(funcName)s() line=%(lineno)d: %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

lb_logger = logging.getLogger("labgoo")
lb_logger.setLevel(lb_logging_level)
lb_logger.addHandler(handler)
