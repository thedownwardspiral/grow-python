import atexit
import threading
import time

import gpiodevice

from . import pwm

PUMP_1_PIN = "PIN11" # 17
PUMP_2_PIN = "PIN13" # 27
PUMP_3_PIN = "PIN15" # 22
PUMP_PWM_FREQ = 10000
PUMP_MAX_DUTY = 0.9

PLATFORMS = {
    "Raspberry Pi 5": ["PIN11", "PIN13", "PIN15"],
    "Raspberry Pi 4": ["GPIO17", "GPIO27", "GPIO22"],
    "Raspberry Pi 3": ["GPIO17", "GPIO27", "GPIO22"],
    "Raspberry Pi 2": ["GPIO17", "GPIO27", "GPIO22"],
    "Raspberry Pi": ["GPIO17", "GPIO27", "GPIO22"],
    "Raspberry Pi Zero 2": ["GPIO17", "GPIO27", "GPIO22"],
    "Raspberry Pi Zero": ["GPIO17", "GPIO27", "GPIO22"],
}

# Detected platform pins (cached after first detection)
_platform_pins = None


def _get_platform_pins():
    """Detect platform and return the list of pump pin names."""
    global _platform_pins
    if _platform_pins is not None:
        return _platform_pins

    # Try to find the platform by checking which one matches
    for platform_name, pins in PLATFORMS.items():
        try:
            chip = gpiodevice.find_chip_by_platform(platform_name)
            if chip is not None:
                _platform_pins = pins
                return _platform_pins
        except Exception:
            continue

    # Fallback to GPIO naming (works for Pi 2/3/4/Zero)
    _platform_pins = ["GPIO17", "GPIO27", "GPIO22"]
    return _platform_pins


global_lock = threading.Lock()


class Pump:
    """Grow pump driver."""

    def __init__(self, channel=1):
        """Create a new pump.

        Uses soft PWM to drive a Grow pump.

        :param channel: One of 1, 2 or 3.

        """
        pins = _get_platform_pins()
        pin_name = pins[channel - 1]

        # Get the GPIO pin using gpiodevice.get_pin (works around get_pins_for_platform bug)
        self._gpio_pin = gpiodevice.get_pin(pin_name, f"pump{channel}", pwm.OUTL)

        self._pwm = pwm.PWM(self._gpio_pin, PUMP_PWM_FREQ)
        self._pwm.start(0)

        pwm.PWM.start_thread()
        atexit.register(pwm.PWM.stop_thread)

        self._timeout = None
        self._speed = 0

    def set_speed(self, speed):
        """Set pump speed (PWM duty cycle)."""
        if speed > 1.0 or speed < 0:
            raise ValueError("Speed must be between 0 and 1")

        if speed == 0:
            global_lock.release()
        elif not global_lock.acquire(blocking=False):
            return False

        self._pwm.set_duty_cycle(PUMP_MAX_DUTY * speed)
        self._speed = speed
        return True

    def get_speed(self):
        """Return Pump speed (PWM duty cycle)."""
        return self._speed

    def stop(self):
        """Stop the pump."""
        if self._timeout is not None:
            self._timeout.cancel()
            self._timeout = None
        self.set_speed(0)

    def dose(self, speed, timeout=0.1, blocking=True, force=False):
        """Pulse the pump for timeout seconds.

        :param timeout: Timeout, in seconds, of the pump pulse
        :param blocking: If true, function will block until pump has stopped
        :param force: Applies only to non-blocking. If true, any previous dose will be replaced

        """

        if blocking:
            if self.set_speed(speed):
                time.sleep(timeout)
                self.stop()
                return True

        else:
            if self._timeout is not None:
                if self._timeout.is_alive():
                    if force:
                        self._timeout.cancel()

            self._timeout = threading.Timer(timeout, self.stop)
            if self.set_speed(speed):
                self._timeout.start()
                return True

        return False
