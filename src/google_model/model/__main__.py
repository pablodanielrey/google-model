import os
import logging

LEVEL = os.environ.get('LOGLEVEL','INFO').upper()
logging.basicConfig(level=LEVEL)

from .GoogleModel import GoogleModel

g = GoogleModel()
g.listen()