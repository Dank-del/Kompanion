from telethon.sessions import StringSession
from telethon import TelegramClient

import os
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.ini")
general = parser["general"]
    
SESSION = general.get("SESSION")
APP_ID = general.get("APP_ID")
API_HASH = general.get("API_HASH")
    
Kompanion = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)