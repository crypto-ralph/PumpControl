import logging
import os

from dotenv import load_dotenv
import time
from domoticz import Domoticz
from PWM import PumpVoltageControl
from control import PumpController
from temperature import TempManager
from config import PWM_PIN, log_format, simulation_enabled
from test.mocks.pump_mock import PumpMock
from test.mocks.temp_mock import mock_temp_manager

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format=log_format,
                    datefmt='%Y-%m-%d %H:%M:%S')

keep_running = True

# Load the environment variables from .env file
load_dotenv()

# Accessing the variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
domoticz_ip = os.getenv('DOMOTICZ_IP')
domoticz_port = os.getenv('DOMOTICZ_PORT')


# Classes initializations
domoticz = Domoticz(username, password, domoticz_ip, domoticz_port)
temp_manager = TempManager(domoticz=domoticz)
pump_control = PumpVoltageControl(PWM_PIN)

if simulation_enabled is True:
    mock_temp_manager(temp_manager)
    pump_mock = PumpMock(temp_manager)

controller = PumpController(pump_control, simulation_enabled)

def main():
    while True:
        temperatures = temp_manager.get_temperatures()
        logger.debug(temperatures)
        for sensor, value in temperatures.items():
            if value is not None:
                logger.info(f"The temperature of {sensor} is {value:.4f} C")

        controller.control_temp(temperatures, pump_mock)
        pump_mock.update()
        time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Terminating...")

