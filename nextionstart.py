import datetime
from time import sleep
import subprocess
import os
import nextion_lib as nxlib
import sys, signal


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def startCar():
    p = None
    logpath = os.path.abspath('./logs')
    if not os.path.exists(logpath):
        os.mkdir(logpath)
    
    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    logfile =  os.path.join(logpath, uniq_filename)
    f = open(logfile,'wb')
    p = subprocess.Popen(['python', '-u', 'manage.py', 'drive'],
                            stdout=f,
                            stderr=subprocess.STDOUT,
                            preexec_fn=os.setsid)
    return f,p


######### make connection to serial UART to read/write NEXTION
ser = nxlib.ser
EndCom = "\xff\xff\xff"
# nxlib.nx_setsys(ser, 'bauds', nxlib.BAUD)  # set default baud (default baud rate of nextion from fabric is 9600)
state = 'Ready'
nxlib.nx_setsys(ser, 'bkcmd',0)            # sets in NEXTION 'no return error/success codes'
nxlib.nx_setcmd_1par(ser, 'page', 0)
nxlib.nx_setText(ser, 0,1,state)

look_touch = 1  # in seconds
while True:
    try:

        touch=ser.read_until(EndCom)

        if  hex(touch[0]) == '0x65':  #  touch event. If it's empty, do nothing
            pageID_touch = touch[1]
            compID_touch = touch[2]
            event_touch = touch[3]
            print("page= {}, component= {}, event= {}".format(pageID_touch,compID_touch,event_touch))

            if (pageID_touch, compID_touch) == (0, 3):  # Start Button pressed
                f,p = startCar()
                state = 'Running'
                nxlib.nx_setcmd_1par(ser, 'page', 1)
                nxlib.nx_setText(ser, 1,1,state)
             
            if (pageID_touch, compID_touch) == (1, 3):  # Stop Button pressed
                print('terminate requested')
                os.killpg(os.getpgid(p.pid), signal.SIGINT)
                p.wait() 
                f.close 
                state = 'Stopped'
                nxlib.nx_setcmd_1par(ser, 'page', 0)
                nxlib.nx_setText(ser, 0,1,state)
    
        sleep(look_touch)  ### timeout the bigger the larger the chance of missing a push
    except:
        if state == 'Running':
            rc = p.poll()
            if rc is not None:
                f.close 
                state = 'Stopped'
                nxlib.nx_setcmd_1par(ser, 'page', 0)
                nxlib.nx_setText(ser, 0,1,'Car crashed')
        sleep(look_touch)
