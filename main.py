#!/usr/bin/python

import platform
from context import Context, Windows, MacOS


def start():
    if platform.system() == 'Windows':
        context1 = Context(Windows())
    if platform.system() == 'Darwin':
        context1 = Context(MacOS())
    context1.execute()


if __name__ == "__main__":
    start()
