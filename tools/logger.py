# Standard library imports
import logging as log

def init_logger(log_level):

    log.basicConfig(level    = log_level    , \
                    filename = 'logfile.log', \
                    filemode = 'w'          , \
                    format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')