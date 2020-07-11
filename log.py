# -*- coding: utf-8 -*-
import time
import logging

import config


# Setting up the logger
log = logging.getLogger('decisoes')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

fileHandler = logging.FileHandler('precedentes_extractor_%s.log' % (time.strftime("%Y-%m-%d %H:%M")))
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
log.addHandler(consoleHandler)

log.setLevel(logging.INFO)
