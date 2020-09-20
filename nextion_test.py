
import time
from time import sleep
import subprocess
import os
import nextion_lib as nxlib

######### make connection to serial UART to read/write NEXTION
ser = nxlib.ser
EndCom = "\xff\xff\xff"
# nxlib.nx_setsys(ser, 'bauds', nxlib.BAUD)  # set default baud (default baud rate of nextion from fabric is 9600)

nxlib.nx_setsys(ser, 'bkcmd',0)            # sets in NEXTION 'no return error/success codes'
print(nxlib.nx_getText(ser, 0, 1))
nxlib.nx_setText(ser, 0,1,'Ready')

# nxlib.nx_setcmd_2par(ser,'tsw','button01',1)     # enable touch events of b0

look_touch = 1  # in seconds
print("detecting serial every {} second(s) ...".format(look_touch))
while True:
    try:
        touch=ser.read_until(EndCom)
        if  hex(touch[0]) == '0x65':  #  touch event. If it's empty, do nothing
            pageID_touch = touch[1]
            compID_touch = touch[2]
            event_touch = touch[3]
            print("page= {}, component= {}, event= {}".format(pageID_touch,compID_touch,event_touch))

            if (pageID_touch, compID_touch) == (0, 2):  # Start Button pressed
                nxlib.nx_setcmd_1par(ser, 'page', 1)
                try:
                    subprocess.Popen(["python",os.path.realpath("manage.py"),"drive"], universal_newlines=True, close_fds=True)
                    nxlib.nx_setcmd_1par(ser, 'page', 2)
                except:
                    print("Error")
                ser.close()
                print("exiting")
                break
        sleep(look_touch)  ### timeout the bigger the larger the chance of missing a push
    except:
        pass
