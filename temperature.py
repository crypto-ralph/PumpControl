import logging
from abc import ABC

from w1thermsensor import W1ThermSensor
from config import sensor1_id, sensor2_id

logger = logging.getLogger(__name__)


class TempSensor(ABC):
    def __init__(self):
        pass


class TempManager:
    def __init__(self):
        try:
            self.sensor1 = W1ThermSensor(sensor_id=sensor1_id)
            self.sensor2 = W1ThermSensor(sensor_id=sensor2_id)
        except:
            logger.error("Could not initialize temp sensor")
            self.sensor1 = None
            self.sensor2 = None

    def get_temperatures(self):
        return {
            "sensor_1": self.sensor1.get_temperature() if self.sensor1 is not None else None,
            "sensor_2": self.sensor2.get_temperature() if self.sensor2 is not None else None,
        }
