#!/usr/bin/env python3

# long running process 
import time
STOPINT = 60
count = 1
st = time.time()
while True:
    time.sleep(0.2)
    print(count)
    count += 1
    if time.time() - st > STOPINT:
        break
