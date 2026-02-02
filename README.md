# Grow HAT Mini

Designed as a tiny valet for your plants, Grow HAT mini will monitor the soil moiture for up to 3 plants, water them with tiny pumps, and show you their health on its small but informative screen. Learn more - https://shop.pimoroni.com/products/grow

## Supported Platforms

| Platform | OS | Status |
|----------|-----|--------|
| Raspberry Pi 4 | Debian Trixie | ✅ Tested |
| Raspberry Pi 4 | Debian Bookworm | ✅ Supported |
| Raspberry Pi 5 | Debian Bookworm | ✅ Supported |

**Requirements:** Python 3.9+, gpiod 2.1.3+

# Installing

You're best using the "One-line" install method.

## One-line (Installs from GitHub)

```
curl -sSL https://get.pimoroni.com/grow | bash
```

**Note** report issues with one-line installer here: https://github.com/pimoroni/get

## Or... Install and configure dependencies from GitHub:

* `git clone https://github.com/pimoroni/grow-python`
* `cd grow-python`
* `sudo ./install.sh`

**Note** Raspbian Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

* Install dependencies:

```
sudo apt install python3-setuptools python3-pip python3-yaml python3-smbus python3-pil python3-spidev python3-libgpiod
```

* Run `sudo pip3 install growhat`

**Note** this won't perform any of the required configuration changes on your Pi, you may additionally need to:

* Enable i2c: `sudo raspi-config nonint do_i2c 0`
* Enable SPI: `sudo raspi-config nonint do_spi 0`
* Add the following to `/boot/config.txt`: `dtoverlay=spi0-cs,cs0_pin=14`

## Monitoring

You should read the following to get up and running with our monitoring script:

* [Using and configuring monitor.py](examples/README.md)
* [Setting up monitor.py as a service](service/README.md)

## Testing

Run unit tests:
```bash
python -m pytest tests/ -v
```

Run QA checks:
```bash
ruff check .
isort --check .
codespell .
```

## Development Setup

```bash
python3 -m venv pimoroni
./pimoroni/bin/pip install -e .
./pimoroni/bin/pip install pytest pytest-cov ruff isort codespell
```

## Help & Support

* GPIO Pinout - https://pinout.xyz/pinout/grow_hat_mini
* Support forums - http://forums.pimoroni.com/c/support
* Discord - https://discord.gg/hr93ByC

# Changelog
0.0.4
-----

* Fix wrong GPIO pin for pump2 on Raspberry Pi 5 (PIN12 -> PIN13)
* Fix PWM thread event never cleared after stop, preventing restart
* Fix PWM destructor crash if constructor fails midway
* Fix Moisture destructor crash if constructor fails midway
* Fix PWM ZeroDivisionError when frequency is zero
* Migrate examples/monitor.py from RPi.GPIO to gpiod for button handling
* Fix PWM initial state mismatch with GPIO configuration
* Fix PWM thread busy-wait consuming 100% CPU
* Fix PWM stop not setting GPIO to inactive state
* Update ST7735 import to use modern lowercase module name
* Replace deprecated fonts.ttf with direct font_roboto import (removes pkg_resources deprecation warning)
* Add setuptools to install.sh dependencies

0.0.3
-----

* Port to gpiod/gpiodevice for Raspberry Pi 5 support
* Migrate to Pillow 11.x compatible API (Debian Trixie)
* Require Python 3.9+ (drop Python 3.7/3.8 support)
* Add Python 3.12 support
* Use stdlib unittest.mock instead of mock package
* Fix uninitialized _speed attribute in Pump class

0.0.2
-----

* Add mutually exclusive locking to pumps to avoid brownout running multiple pumps at once

0.0.1
-----

* Initial Release
