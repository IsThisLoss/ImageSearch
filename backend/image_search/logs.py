import logging
import logging.config

LOGGER_NAME = 'image_search'
LOG_FORMAT = '%(levelprefix)s | %(asctime)s | %(message)s'
LOG_LEVEL = 'INFO'

LOG_CONFIG = {
    # Logging config
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
    }
}

def init():
    logging.config.dictConfig(LOG_CONFIG)


def get_logger():
    return logging.getLogger('image_search')
