#!/usr/bin/env python3

# long running process 
import time
import sys, signal

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

STOPINT = 60
count = 1
st = time.time()
while True:
    time.sleep(0.2)
    print(count)
    count += 1
    if time.time() - st > STOPINT:
        break
