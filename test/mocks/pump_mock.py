from temperature import TempManager
from test.mocks.temp_mock import TempSensorMock


class PumpMock:
    def __init__(self, temp_manager_mocked: TempManager):
        self.power = 0
        # if (not isinstance(temp_manager_mocked.sensors[0], TempSensorMock)
        #         and not isinstance(temp_manager_mocked.sensors[1], TempSensorMock)):
        #     raise Exception("Temp Manager has to be mocked")
        self.temp_manager = temp_manager_mocked

    def set_power(self, value: int):
        if value in range(0, 11):
            self.power = value

    def update(self):
        temp = self.temp_manager.sensors[1].temperature
        self.temp_manager.sensors[1].temperature = temp + self.power * 0.15
        self.temp_manager.sensors[1].temperature -= 0.13
