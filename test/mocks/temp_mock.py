from temperature import TempManager


def mock_temp_manager(manager: TempManager):
    manager.sensor1 = TempSensorMock()
    manager.sensor2 = TempSensorMock()


class TempSensorMock:
    def __init__(self, temp: int = 24):
        self.temperature = temp

    def get_temperature(self) -> int:
        return self.temperature
