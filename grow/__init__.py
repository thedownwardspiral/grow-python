__version__ = '0.0.5'

import atexit
import threading
import time

import gpiodevice

from . import pwm

PLATFORMS = {
    "Raspberry Pi 5": "PIN33",
    "Raspberry Pi 4": "GPIO13",
    "Raspberry Pi 3": "GPIO13",
    "Raspberry Pi 2": "GPIO13",
    "Raspberry Pi": "GPIO13",
    "Raspberry Pi Zero 2": "GPIO13",
    "Raspberry Pi Zero": "GPIO13",
}

# Detected platform piezo pin (cached after first detection)
_piezo_pin = None


def _get_piezo_pin():
    """Detect platform and return the piezo pin name."""
    global _piezo_pin
    if _piezo_pin is not None:
        return _piezo_pin

    # Try to find the platform by checking which one matches
    for platform_name, pin in PLATFORMS.items():
        try:
            chip = gpiodevice.find_chip_by_platform(platform_name)
            if chip is not None:
                _piezo_pin = pin
                return _piezo_pin
        except Exception:
            continue

    # Fallback to GPIO naming (works for Pi 2/3/4/Zero)
    _piezo_pin = "GPIO13"
    return _piezo_pin


class Piezo():
    def __init__(self, gpio_pin=None):

        if gpio_pin is None:
            pin_name = _get_piezo_pin()
            gpio_pin = gpiodevice.get_pin(pin_name, "piezo", pwm.OUTL)
        elif isinstance(gpio_pin, str):
            gpio_pin = gpiodevice.get_pin(gpio_pin, "piezo", pwm.OUTL)

        self.pwm = pwm.PWM(gpio_pin)
        self._timeout = None
        pwm.PWM.start_thread()
        atexit.register(pwm.PWM.stop_thread)

    def frequency(self, value):
        """Change the piezo frequency.

        Loosely corresponds to musical pitch, if you suspend disbelief.

        """
        self.pwm.set_frequency(value)

    def start(self, frequency):
        """Start the piezo.

        Sets the Duty Cycle to 50%

        """
        self.pwm.start(frequency=frequency, duty_cycle=0.5)

    def stop(self):
        """Stop the piezo.

        Sets the Duty Cycle to 0%

        """
        self.pwm.stop()

    def beep(self, frequency=440, timeout=0.1, blocking=True, force=False):
        """Beep the piezo for time seconds.

        :param freq: Frequency, in hertz, of the piezo
        :param timeout: Time, in seconds, of the piezo beep
        :param blocking: If true, function will block until piezo has stopped

        """
        if blocking:
            self.start(frequency=frequency)
            time.sleep(timeout)
            self.stop()
            return True
        else:
            if self._timeout is not None:
                if self._timeout.is_alive():
                    if force:
                        self._timeout.cancel()
                    else:
                        return False
            self._timeout = threading.Timer(timeout, self.stop)
            self.start(frequency=frequency)
            self._timeout.start()
            return True
