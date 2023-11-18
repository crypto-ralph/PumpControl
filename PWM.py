import RPi.GPIO as GPIO
import logging

logger = logging.getLogger("PWM")


voltage_levels = {
    0: 0,
    1: 15,
    2: 30,
    3: 45,
    4: 55,
    5: 67,
    6: 76,
    7: 85,
    8: 90,
    9: 95,
    10: 100,
}


def _check_voltage_input(voltage: int) -> bool:
    if voltage in range(0, 11):
        return True
    else:
        logger.error(f"Wrong voltage: {voltage}")
        return False


class PumpVoltageControl:
    def __init__(self, pwm_pin: int, init_voltage: int = 0, init_freq: int = 1000):
        self.pwm_pin = pwm_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pwm_pin, init_freq)
        if _check_voltage_input(init_voltage):
            self.start_pwm(voltage_levels[init_voltage])

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()

    def start_pwm(self, init_duty: int):
        self.pwm.start(init_duty)

    def set_voltage(self, voltage: int):
        if _check_voltage_input(voltage):
            logger.debug(f"Voltage set to {voltage}. Duty cycle: {voltage_levels[voltage]}")
            self.pwm.ChangeDutyCycle(voltage_levels[voltage])
