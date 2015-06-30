from cx_Freeze import setup, Executable
import sys


target_name = 'esptool-gui'
app_version = '0.1.0'
app_description = 'GUI wrapper for ESP8266 ROM Bootloader utility esptool.py'
app_icon = '..\\esptool_gui\\rc\\app_icon.ico'


# Dependencies are automatically detected, but it might need
# fine tuning.
path = sys.path
path.append('..')

buildOptions = dict(packages = ['esptool_gui'],
                    excludes = [],
                    path = path,
                    include_files = [('..\\esptool_gui\\rc', 'rc'),
                                     ('build_esptool', 'esptool')])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('..\\esptool-gui.py', base=base, targetName = target_name + '.exe',
               icon = app_icon)
]


# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    ("DesktopShortcut",                # Shortcut
     "DesktopFolder",                  # Directory_
     "esptool GUI",                    # Name
     "TARGETDIR",                      # Component_
     "[TARGETDIR]%s.exe" % target_name,# Target
     None,                             # Arguments
     app_description,                  # Description
     None,                             # Hotkey
     None,                             # Icon
     None,                             # IconIndex
     None,                             # ShowCmd
     'TARGETDIR'                       # WkDir
     )
]
# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}
# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}


setup(name=target_name,
      version = app_version,
      description = app_description,
      options = dict(build_exe=buildOptions, bdist_msi=bdist_msi_options),
      executables = executables)
