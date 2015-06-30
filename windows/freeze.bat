c:\python27\python.exe setup_esptool.py build
c:\python34\python.exe setup_esptool_gui.py bdist_msi
copy /y dist\*.msi .
rd /s /q build_esptool build dist
