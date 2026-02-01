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
