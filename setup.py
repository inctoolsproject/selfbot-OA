import ctypes
import os
import sys

def is_user_admin():
    """Returns True if the program was ran as administrator"""
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

if not is_user_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    quit()

required_modules = [
    "requests",
    "bs4",
    "pyyaml",
    "dhooks",
    "tqdm",
    "dhooks",
    'datetime',
    'discord'
]

for module in required_modules:
    os.system("python -m pip install " + module)

os.system("cls")

input("""
All the modules have been successfully installed\n
Now, edit the config file and launch the bot""")