import logging
from datetime import datetime


def logger():
    # Logging

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
                        level=logging.DEBUG,
                        format=LOG_FORMAT)
