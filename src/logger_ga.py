"""
class to generate loggin
"""
import logging
import time
import os
from pathlib import Path

class writeLog():
    def __init__(self, message = None):
        self.message = message
    
    def write_log(self):
        Path("./src/logs").mkdir(parents=True, exist_ok=True)

        logging.basicConfig(filename='./src/logs/ga-'+time.strftime("%Y%m%d")+'.log',level=logging.ERROR)
        logging.error(self.message)
        