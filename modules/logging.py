<<<<<<< HEAD
import logging
from datetime import datetime


def logger(input_log_level=None):
    # Logging

    if input_log_level == 'DEBUG':
        logger_level = logging.DEBUG
    elif input_log_level == 'INFO':
        logger_level = logging.INFO
    elif input_log_level == 'WARNING':
        logger_level = logging.WARNING
    elif input_log_level == 'ERROR':
        logger_level = logging.ERROR
    elif input_log_level == 'CRITICAL':
        logger_level = logging.CRITICAL

    # Current Timestamp
    ts = datetime.now()
    ts = ts.strftime("%Y-%m-%d %H:%M:%S")
    ts = ts.replace('-', '')
    ts = ts.replace(':', '')
    ts = ts.replace(' ', '_')
    ts = 'logs\\' + ts + '.log'

    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename=ts,
                        filemode='a',
                        level=logger_level,
                        format=LOG_FORMAT)
=======
import logging
from datetime import datetime


def logger(input_log_level=None):
    # Logging

    if input_log_level == 'DEBUG':
        logger_level = logging.DEBUG
    elif input_log_level == 'INFO':
        logger_level = logging.INFO
    elif input_log_level == 'WARNING':
        logger_level = logging.WARNING
    elif input_log_level == 'ERROR':
        logger_level = logging.ERROR
    elif input_log_level == 'CRITICAL':
        logger_level = logging.CRITICAL

    # Current Timestamp
    ts = datetime.now()
    ts = ts.strftime("%Y-%m-%d %H:%M:%S")
    ts = ts.replace('-', '')
    ts = ts.replace(':', '')
    ts = ts.replace(' ', '_')
    ts = 'logs\\' + ts + '.log'

    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename=ts,
                        filemode='a',
                        level=logger_level,
                        format=LOG_FORMAT)
>>>>>>> 02fbe3340762954ee38b54461631d0e36a0878b4
