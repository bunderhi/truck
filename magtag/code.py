import time
import sys
import ipaddress
import wifi
import socketpool
import adafruit_requests
from adafruit_magtag.magtag import MagTag

magtag = MagTag()

RED = 0x880000
GREEN = 0x008800
BLUE = 0x000088
YELLOW = 0x884400
CYAN = 0x0088BB
MAGENTA = 0x9900BB
WHITE = 0x888888

button_tones = (1047, 1318, 1568, 2093)

def blinkTone(color, duration=0.25):
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill(color)
    magtag.peripherals.play_tone(button_tones[0], duration)
    magtag.peripherals.neopixel_disable = True

# jetracer WS URL
DRIVE_URL = "http://jetracer.local:8887/drive"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print(
        "\t%s\t\tRSSI: %d\tChannel: %d"
        % (str(network.ssid, "utf-8"), network.rssi, network.channel)
    )
    net = str(network.ssid, "utf-8")
    if net == secrets["ssid0"]:
        passwd = secrets["password0"]
        break
    if net == secrets["ssid1"]:
        passwd = secrets["password1"]
wifi.radio.stop_scanning_networks()
if passwd is not None:
    print("Connecting to %s" % net)
    wifi.radio.connect(net, passwd)
    print("Connected to %s!" % net)
    print("My IP address is", wifi.radio.ipv4_address)
else:
    print("Error: Network not found")
    sys.exit()
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)
data = {}
response = None
runstate = 'initializing'

magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=3,
)
magtag.set_text('Connected:'+net)
time.sleep(1.0)
response = requests.get(DRIVE_URL)
data = response.json()
print(data)
print(response.status_code)
response.close()
runstate = data["RunState"]
magtag.set_text(runstate)

while True:
    if magtag.peripherals.button_a_pressed:
        print("Button pressed")
        if runstate == 'ready':
            myobj = {"RunCmd": "start"}
            x = requests.post(DRIVE_URL, json=myobj)
        elif runstate == 'running':
            myobj = {"RunCmd": "stop"}
            x = requests.post(DRIVE_URL, json=myobj)
            magtag.set_text(runstate)
        # Blink the neopixels
        blinkTone(YELLOW)
        # refresh runstate from server
        response = requests.get(DRIVE_URL)
        data = response.json()
        print(data)
        print(response.status_code)
        response.close()
        runstate = data["RunState"]
        magtag.set_text(runstate)
    time.sleep(0.01)
