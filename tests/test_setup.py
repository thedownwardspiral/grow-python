import mock


def test_moisture_setup(gpiod, gpiodevice, smbus2):
    from datetime import timedelta

    from grow.moisture import Moisture

    ch1 = Moisture(channel=1)
    ch2 = Moisture(channel=2)
    ch3 = Moisture(channel=3)


def test_moisture_read(gpiod, gpiodevice, smbus2):
    from grow.moisture import Moisture

    assert Moisture(channel=1).saturation == 1.0
    assert Moisture(channel=2).saturation == 1.0
    assert Moisture(channel=3).saturation == 1.0

    assert Moisture(channel=1).moisture == 0
    assert Moisture(channel=2).moisture == 0
    assert Moisture(channel=3).moisture == 0


def test_pump_setup(gpiod, gpiodevice, smbus2):
    from grow.pump import PUMP_PWM_FREQ, Pump
    from grow.pwm import PWM

    ch1 = Pump(channel=1)
    ch2 = Pump(channel=2)
    ch3 = Pump(channel=3)

    # Threads. Not even once.
    PWM.stop_thread()

