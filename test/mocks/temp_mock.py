from temperature import TempManager


def mock_temp_manager(manager: TempManager):
        manager.sensors = [TempSensorMock("outside_temp", 3),
                           TempSensorMock("water_temp", 10)]


class TempSensorMock:
    def __init__(self, name: str, temp: float = 24.0):
        self.name = name
        self.temperature = temp

    def get_temperature(self) -> float:
        return self.temperature
