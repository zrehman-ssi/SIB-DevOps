import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def get_logger(name):
    log_format = '%(asctime)s:%(name)8s:%(levelname)s:%(message)s'
    time_rotating_file_handler = TimedRotatingFileHandler("logs/SIB.log", when="midnight", interval=1)
    time_rotating_file_handler.setLevel(logging.DEBUG)
    time_rotating_file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(time_rotating_file_handler)
    return logging.getLogger(name)