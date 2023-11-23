import logging
from typing import Optional

from PWM import PumpVoltageControl
from config import temperature_table, temp_diff_table
from test.mocks.pump_mock import PumpMock

logger = logging.getLogger(__name__)


def interpolate(x0, y0, x1, y1, x):
    """Linearly interpolate to find y at x."""
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def approximate_target_temp(outside_temp: float) -> Optional[float]:
    """Approximate target water temperature for a given outside temperature."""
    # Sort the keys of the temperature table
    sorted_temps = sorted(temperature_table.keys())

    if max(temperature_table.keys()) < outside_temp < min(temperature_table.keys()):
        return None

    # Find the bracketing temperatures
    for i in range(len(sorted_temps) - 1):
        if sorted_temps[i] <= outside_temp <= sorted_temps[i + 1]:
            x0, x1 = sorted_temps[i], sorted_temps[i + 1]
            y0, y1 = temperature_table[x0], temperature_table[x1]
            return interpolate(x0, y0, x1, y1, outside_temp)


def nearest_value(temp):
    keys = list(temp_diff_table.keys())
    nearest_key = min(keys, key=lambda k: abs(k - temp))

    if temp > nearest_key != keys[-1] and (temp - nearest_key) >= 2:
        index = keys.index(nearest_key)
        nearest_key = keys[index + 1]
    return temp_diff_table[nearest_key]


class PumpController:
    def __init__(self, pump_control: PumpVoltageControl):
        self.target_temp = 0
        self.pump_power = 0
        self.pump_control = pump_control
        self.delay_time = 15
        self.current_time = 12

    def control_temp(self, temperatures: dict[str, float], pump_mock: Optional[PumpMock] = None):
        outside_temp = temperatures["outside_temp"]
        water_temp = temperatures["water_temp"]

        indoor_temps = [temperature for name, temperature in temperatures.items() if "indoor" in name]
        min_indoor_temp = min(indoor_temps) if indoor_temps != [] else None

        pump_power_prev = self.pump_power

        self.target_temp = approximate_target_temp(outside_temp)
        logger.debug(f"Interpolated target temp: {self.target_temp}")

        self.current_time += 1

        if self.target_temp is None:
            return

        if self.current_time > self.delay_time:
            logger.debug(f"Power: {self.pump_power}")

            # fast heating check
            if min_indoor_temp is not None and min_indoor_temp < 19:
                logger.info("Fast heating activated due to low indoor temp")
                self.pump_power = 10
            else:
                diff_value = self.target_temp - water_temp
                if diff_value > 0:
                    self.pump_power = nearest_value(diff_value)
                else:
                    if self.pump_power >= 0:
                        self.pump_power -= 1
                logger.debug(f"Power changed to {self.pump_power}")
                self.current_time = 0

            if self.pump_power != pump_power_prev:
                self.pump_control.set_voltage(self.pump_power)
                if pump_mock is not None:
                    pump_mock.set_power(self.pump_power)
