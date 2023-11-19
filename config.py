import logging

log_format = "%(asctime)s.%(msecs)03d [%(levelname)-8s]:%(name)s:%(message)s"
formatter = logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S')

simulation_enabled = False

control_interval = 2

PWM_PIN = 18

temperature_sensors = [
    {
        "name": "outside_temp",
        "type": "DS18B20",
        "sensor_id": "00000453e703",
    },
    {
        "name": "water_temp",
        "type": "DS18B20",
        "sensor_id": "000004548229",
    },
    {
        "name": "domoticz_test_temp",
        "type": "Domoticz",
        "sensor_idx": "1",
    },
]

temperature_table = {
    -20: 58,
    -10: 48,
    0: 42,
    10: 32,
    15: 30,
}


