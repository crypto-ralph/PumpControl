from temperature import TempManager


def mock_temp_manager(manager: TempManager):
    manager.sensor1 = TempSensorMock()
    # manager.sensor2 = TempSensorMock()


class TempSensorMock:
    def __init__(self, temp: float = 24.0):
        self.temperature = temp

    def get_temperature(self) -> float:
        return self.temperature
