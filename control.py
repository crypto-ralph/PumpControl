import logging
from typing import Optional

from PWM import PumpVoltageControl
from config import temperature_table
from test.mocks.pump_mock import PumpMock

logger = logging.getLogger(__name__)


def interpolate(x0, y0, x1, y1, x):
    """Linearly interpolate to find y at x."""
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def approximate_target_temp(outside_temp: float):
    """Approximate target water temperature for a given outside temperature."""
    # Sort the keys of the temperature table
    sorted_temps = sorted(temperature_table.keys())

    # Find the bracketing temperatures
    for i in range(len(sorted_temps) - 1):
        if sorted_temps[i] <= outside_temp <= sorted_temps[i + 1]:
            x0, x1 = sorted_temps[i], sorted_temps[i + 1]
            y0, y1 = temperature_table[x0], temperature_table[x1]
            return interpolate(x0, y0, x1, y1, outside_temp)

    # If outside temperature is above highest value in the table
    if outside_temp > max(temperature_table.keys()):
        return None

    # If outside temperature is below lowest value in the table
    return "Temperature too low for approximation"


class PumpController:
    def __init__(self, pump_control: PumpVoltageControl):
        self.target_temp = 0
        self.pump_power = 0
        self.pump_control = pump_control
        self.delay_time = 10
        self.current_time = 12

    def control_temp(self, temperatures: dict, pump_mock: Optional[PumpMock] = None):
        outside_temp = temperatures["outside_temp"]
        water_temp = temperatures["water_temp"]

        pump_power_prev = self.pump_power

        self.target_temp = approximate_target_temp(outside_temp)
        logger.debug(f"Interpolated target temp: {self.target_temp}")

        self.current_time += 1

        if self.target_temp is None:
            return

        if (water_temp < self.target_temp
                and self.pump_power < 10
                and self.current_time > self.delay_time):
            self.pump_power += 1
            logger.debug(f"Power: {self.pump_power}")
            self.current_time = 0
        if water_temp >= self.target_temp:
            self.pump_power = 0
            self.current_time = 0

        if self.pump_power != pump_power_prev:
            self.pump_control.set_voltage(self.pump_power)
            if pump_mock is not None:
                pump_mock.set_power(self.pump_power)
