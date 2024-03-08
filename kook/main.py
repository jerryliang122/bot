from test import world
from khl import Message, Bot
import sys
import os
import logging

logging.basicConfig(level="INFO")

## websocket
bot = Bot(token=os.environ.get("kook_token"))
