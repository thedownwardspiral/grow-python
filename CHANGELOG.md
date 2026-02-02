0.0.5
-----

* Add platform support for Raspberry Pi 1, Pi 2, Pi 3, Pi Zero, and Pi Zero 2
* Work around gpiodevice.get_pins_for_platform bug that caused "GPIO busy" errors on Pi Zero
* Fix pdoc documentation generation failing due to local source import
* Document ARMv6 system package requirements (Pi 1, Pi Zero need python3-numpy, python3-pil)

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
