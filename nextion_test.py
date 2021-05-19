
import time
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

# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
CPU = subprocess.check_output(cmd, shell = True )
cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
MemUsage = subprocess.check_output(cmd, shell = True )
cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
Disk = subprocess.check_output(cmd, shell = True )


netstat = get_ip_address('wlan0')
if netstat is not None:
    netstattxt = netstat
else:
    netstattxt = 'Down'

freememtxt = str(MemUsage.decode('utf-8'))
freedisktxt = str(Disk.decode('utf-8'))

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
