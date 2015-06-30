# esptool-gui
GUI wrapper for ESP8266 ROM Bootloader utility [esptool.py](https://github.com/themadinventor/esptool)

You can create any number of configurations (e.g. for several modules or SDKs or just
for several projects, etc...)<br>
To add a new configuration just modify current value of the 'Configuration' combobox.<br>
Current configuration will be saved on exit or when the 'Save' button will be pressed.<br>
You can delete any existing configuration (including 'Default') except the last existing one.

**Windows** users can use the simple [msi installer](https://github.com/remico/esptool-gui/raw/master/windows/esptool-gui-0.1.0-win32.msi)
from `windows` directory to install prebuilt binaries.
You need not have any *Python* on your PC in this approach.

For **Linux** users:
* `esptool.py` should be available in `$PATH`
* `esptool-gui` uses python3 while `esptool.py` uses python2, so the both need to be installed
* Default port is */dev/ttyUSB0*
