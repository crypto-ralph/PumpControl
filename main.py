import logging
import os

from dotenv import load_dotenv
import threading
import time
import sys
import select

from domoticz import Domoticz
from PWM import PumpVoltageControl
from control import PumpController
from temperature import TempManager
from config import PWM_PIN, log_format
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


home_heating = 30

# Classes initializations
domoticz = Domoticz(username, password, domoticz_ip, domoticz_port)
temp_manager = TempManager(domoticz=domoticz)
pump_control = PumpVoltageControl(PWM_PIN)
controller = PumpController(pump_control)

mock_temp_manager(temp_manager)
pump_mock = PumpMock(temp_manager)

controller.temp_target = 40


def wait_for_input_thread():
    global keep_running
    while keep_running:
        try:
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                value = sys.stdin.readline().strip()
                try:
                    value = int(value)
                    pump_control.set_voltage(value)
                    pump_mock.set_power(value)
                except ValueError:
                    logger.error(f"Wrong input value: {value}")
        except EOFError:
            break


def main():
    while True:
        temperatures = temp_manager.get_temperatures()
        for sensor, value in temperatures.items():
            if value is not None:
                logger.info(f"The temperature of {sensor} is {value:.4f} C")

        controller.control_temp(temperatures, pump_mock)
        pump_mock.update()
        time.sleep(2)


if __name__ == "__main__":
    # input_thread = threading.Thread(target=wait_for_input_thread)
    try:
        # input_thread.start()
        main()
    except KeyboardInterrupt:
        logger.info("Terminating...")
        keep_running = False  # Signal the thread to stop
        # input_thread.join()  # Wait for the thread to finish
