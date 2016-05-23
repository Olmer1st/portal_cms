#!/usr/bin/env python
# coding=utf-8

import import_tools.extract_data  as ed
import signal
import sys


def signal_handler(signal, frame):
    ed.stop_process()
    sys.exit(0)

def main(args):
    ed.start_process()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv)
    print('Press Ctrl+C')
    signal.pause()




