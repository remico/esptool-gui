from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], build_exe = 'build_esptool')

base = 'Console'

executables = [
    Executable('..\\..\\esptool\\esptool.py', base=base, targetName = 'esptool.exe')
]

setup(name='esptool',
      version = '0.1.0',
      description = 'ESP8266 ROM Bootloader utility',
      options = dict(build_exe = buildOptions),
      executables = executables)
