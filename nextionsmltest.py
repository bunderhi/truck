import datetime
from time import sleep
import subprocess
import os
import nextion_lib as nxlib


def get_ip_address(interface):
    state = get_network_interface_state(interface)
    if state == 'down' or state == None:
        return None

    cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
    return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]


def get_network_interface_state(interface):
    if not os.path.exists('/sys/class/net/%s/operstate' % interface):
        #print("%s file does NOT exist" % interface)
        return None

    try:
        status = subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[:-1]
    except Exception as err:
        print("Exception: {0}".format(err))
        return None
    else:
        return status

def startCar():
    p = None
    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    f = open(uniq_filename,'wb')
    p = subprocess.Popen(['python', '-u', '-m', 'manage.py', 'drive'],
                            stdout=f,
                            stderr=subprocess.STDOUT)
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
                #f,p = startCar()
                state = 'Running'
                nxlib.nx_setcmd_1par(ser, 'page', 1)
                nxlib.nx_setText(ser, 1,1,state)
             
            if (pageID_touch, compID_touch) == (1, 3):  # Stop Button pressed
                #p.terminate
                #p.wait
                #print('== subprocess exited with rc =',p.returncode)
                #f.close 
                state = 'Stopped'
                nxlib.nx_setcmd_1par(ser, 'page', 0)
                nxlib.nx_setText(ser, 0,1,state)
        
        #if state == 'running':
        #    rc = p.poll()
        #    if rc is not None:
        #        state = 'Stopped'
        #        nxlib.nx_setText(ser, 0,1,'Car stopped rc='+rc)
        #        nxlib.nx_setText(ser, 1,1,'Car stopped rc='+rc)
        #        nxlib.nx_setcmd_1par(ser, 'page', 0)

        netstat = get_ip_address('wlan0')
        if netstat is not None:
            netstattxt = netstat
        else:
            netstattxt = 'Network Down'
        nxlib.nx_setText(ser, 0,2,netstattxt)
        nxlib.nx_setText(ser, 1,2,netstattxt)

        sleep(look_touch)  ### timeout the bigger the larger the chance of missing a push
    except:
        pass
