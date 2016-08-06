from cx_Freeze import setup, Executable

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
	("DesktopShortcut",			# Shortcut
	 "DesktopFolder",			# Directory_
	 "Mud",		  				# Name
	 "TARGETDIR",				# Component_
	 "[TARGETDIR]mud.exe",		# Target
	 None,						# Arguments
	 None,						# Description
	 None,						# Hotkey
	 None,						# Icon
	 None,						# IconIndex
	 None,						# ShowCmd
	 'TARGETDIR'				# WkDir
	 )
	]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages = ["pygame", "sys", "string", "multiprocessing", "traceback", "random", "mud2"], 
				excludes = [],
				include_files = ["README.txt", "mudico.ico", "basica.ttf", "bells.ogg", 
				"bg1.png", "birds.ogg", "cave.ogg", "credits.ogg", "dark.ogg", 
				"errorlog.txt", "figure.png", "main.ogg", "menu.ogg", "plane.ogg", 
				"plane5050.png", "river.ogg", "top6.png", "vcr.ttf", "whispers.ogg"],
				)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
	Executable('mudpygame.py', base=base, shortcutName="Mud", shortcutDir="DesktopFolder", targetName = 'mud.exe', icon='mudico.ico')
]

setup(name='Mud',
	  version = '1.0',
	  description = 'A text adventure about confronting an impossible situation.',
	  options = dict(build_exe = buildOptions, bdist_msi = bdist_msi_options),
	  executables = executables)
