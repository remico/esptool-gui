# esptool-gui
GUI wrapper for ESP8266 ROM Bootloader utility [esptool.py](https://github.com/themadinventor/esptool)

To add a new configuration just modify current value of the 'Configuration' combobox.<br>
The configuration will be saved on exit or when the 'Save' button will be pressed.<br>
You can delete any existing configuration (including 'Default') except the last existing one.

* `esptool.py` should be available in `$PATH`
* `esptool-gui` uses python3 while `esptool.py` uses python2, so the both need to be installed
* Default port is */dev/ttyUSB0*
