#!/usr/bin/python

import sys
import subprocess
import pkg_resources
import platform
from context import Context, Windows, MacOS

required = {'lxml'}


def start():
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

    if platform.system() == 'Windows':
        context1 = Context(Windows())
    if platform.system() == 'Darwin':
        context1 = Context(MacOS())
    context1.execute()


if __name__ == "__main__":
    start()
