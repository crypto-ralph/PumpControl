from temperature import TempManager
from test.mocks.temp_mock import TempSensorMock


class PumpMock:
    def __init__(self, temp_manager_mocked: TempManager):
        self.power = 0
        if (not isinstance(temp_manager_mocked.sensor1, TempSensorMock)
                and not isinstance(temp_manager_mocked.sensor2, TempSensorMock)):
            raise Exception("Temp Manager has to be mocked")
        self.temp_manager = temp_manager_mocked

    def set_power(self, value: int):
        if value in range(0, 11):
            self.power = value

    def update(self):
        temp = self.temp_manager.sensor2.temperature
        self.temp_manager.sensor2.temperature = temp + self.power * 0.15
        self.temp_manager.sensor2.temperature -= 0.13
