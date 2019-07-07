# Standard library imports
import logging as log

def init_logger(log_level):

    log.basicConfig(level    = log_level          , \
                    filename = 'logfile.log'      , \
                    filemode = 'w'                , \
                    datefmt  = '%Y-%m-%d %H:%M:%S', \
                    format   = '[%(asctime)s] - %(lineno)4d - %(name)s - [%(levelname)s] - %(message)s')