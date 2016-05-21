#!/usr/bin/env python
# coding=utf-8

import import_tools.extract_data  as ed
import signal
import sys


def signal_handler(signal, frame):
    ed.stop_process()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
ed.start_process()
print('Press Ctrl+C')
signal.pause()

