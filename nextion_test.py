
import time
from time import sleep
import nextion_lib as nxlib

######### make connection to serial UART to read/write NEXTION
ser = nxlib.ser

nxlib.nx_setsys(ser, 'bauds', nxlib.BAUD)  # set default baud (default baud rate of nextion from fabric is 9600)
nxlib.nx_setsys(ser, 'bkcmd',0)            # sets in NEXTION 'no return error/success codes'
nxlib.nx_setcmd_1par(ser,'page',0)         # sets page 0  
EndCom = "\xff\xff\xff"                    # 3 last bits to end serial communication

nxlib.nx_setText(ser, 0,0,'Ready')
nxlib.nx_setcmd_2par(ser,'tsw','b0',1)     # enable touch events of b0

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

            if (pageID_touch, compID_touch) == (0, 0):  # Start Button pressed
                nxlib.nx_setcmd_1par(ser, 'page', 1)
        sleep(look_touch)  ### timeout the bigger the larger the chance of missing a push
    except:
        pass

