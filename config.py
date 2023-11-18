import logging

log_format = "%(asctime)s.%(msecs)03d [%(levelname)-8s]:%(name)s:%(message)s"
formatter = logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S')

PWM_PIN = 18
sensor1_id = "00000453e703"
sensor2_id = "000004548229"

temperature_table = {
    -20: 58,
    -10: 48,
    0: 42,
    10: 32,
    15: 30,
    20: None,
}


