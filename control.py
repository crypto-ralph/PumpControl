from PWM import PumpVoltageControl
from test.mocks.pump_mock import PumpMock


class PumpController:
    def __init__(self, pump_control: PumpVoltageControl):
        self.temp_target = 0
        self.pump_power = 0
        self.pump_control = pump_control

    def control_temp(self, current_temp: float, pump_mock: PumpMock):
        if current_temp < self.temp_target and self.pump_power <= 10:
            self.pump_power += 1
        if current_temp >= self.temp_target:
            self.pump_power = 0

        self.pump_control.set_voltage(self.pump_power)
        pump_mock.set_power(self.pump_power)
