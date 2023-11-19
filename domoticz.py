import urllib.parse
from typing import Optional

import requests
import json
import enum
import logging

logger = logging.getLogger(__name__)


class LogLevel(enum.Enum):
    NORMAL = 1
    STATUS = 2
    ERROR = 4


class Domoticz:
    def __init__(self, _username, _password, _domoticz_ip, _domoticz_port):
        self.url = f"https://{_username}:{_password}@{_domoticz_ip}:{_domoticz_port}/json.htm"

    def domoticz_get(self, params: dict) -> Optional[str]:
        response = requests.get(self.url, params, verify=False)
        # logger.debug(f"Response code: {response.status_code}. Message: {response.text}")
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Wrong status: {response.status_code}")
            return None

    def get_unit_data(self, idx: int) -> float:
        params = {
            "type": "command",
            "param": "getdevices",
            "rid": idx,
        }
        result = json.loads(self.domoticz_get(params))
        return float(result["result"][0]["Data"][:-2])

    def send_log(self, message: str, level: LogLevel = LogLevel.NORMAL):
        params = {
            "type": "command",
            "param": "addlogmessage",
            "message": urllib.parse.quote(message),
            "level": level.value,
        }
        response = self.domoticz_get(params)

        return response
