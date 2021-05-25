# long running process 
import time
STOPINT = 200
st = time.time()
while True:
    time.sleep(0.2)
    print('*')
    if time.time() - st > STOPINT:
        break
