import logging
from abc import ABC, abstractmethod

from w1thermsensor import W1ThermSensor
from domoticz import Domoticz
from config import sensor1_id, sensor2_id

logger = logging.getLogger(__name__)


class TempSensor(ABC):
    """
    Abstract base class representing a temperature sensor.

    :param name: A string representing the name of the sensor.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_temperature(self) -> float:
        """
        Abstract method to get the current temperature from the sensor.

        :return: The current temperature as a float.
        :rtype: float
        """
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"TempSensor(name='{self.name}')"


class DomoticzSensor(TempSensor):
    """
    Represents a temperature sensor that fetches data from a Domoticz unit.

    :param name: The name of the sensor.
    :param sensor_idx: The index of the sensor in the Domoticz system.
    :param domoticz: A Domoticz instance to interact with the Domoticz API.
    """

    def __init__(self, name: str, sensor_idx: int, domoticz: Domoticz):
        super().__init__(name)
        self.sensor_idx = sensor_idx
        self.domoticz = domoticz

    def get_temperature(self):
        return self.domoticz.get_unit_data(self.sensor_idx)


class DS18Sensor(TempSensor):
    """
    Represents a DS18B20 temperature sensor connected to Raspberry Pi.

    :param name: The name of the sensor.
    :param sensor_id: The unique identifier for the sensor.
    """

    def __init__(self, name: str, sensor_id: str):
        super().__init__(name)
        self.sensor = W1ThermSensor(sensor_id=sensor_id)

    def get_temperature(self):
        return self.sensor.get_temperature()


class TempManager:
    """
    Manages multiple temperature sensors, providing an interface to get temperatures.

    The TempManager initializes two DS18Sensor instances by default. If initialization fails,
    the corresponding sensor attributes are set to None.
    """

    def __init__(self):
        try:
            self.sensor1 = DS18Sensor(name="Outside_temp", sensor_id=sensor1_id)
        except:
            logger.error("Could not initialize temp sensor 1")
            self.sensor1 = None

        try:
            self.sensor2 = DS18Sensor(name="Generic_temp", sensor_id=sensor2_id)
        except:
            logger.error("Could not initialize temp sensor 2")
            self.sensor2 = None

    def get_temperatures(self) -> dict[str, float]:
        """
        Retrieves the temperatures from the managed sensors.

        :return: A dictionary with the sensor names as keys and their respective temperatures as values.
                 If a sensor is not initialized, its value is set to None.
        """
        return {
            "sensor_1": self.sensor1.get_temperature() if self.sensor1 is not None else None,
            "sensor_2": self.sensor2.get_temperature() if self.sensor2 is not None else None,
        }