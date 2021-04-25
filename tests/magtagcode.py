import ipaddress
import wifi
import socketpool
import adafruit_requests

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
wifi.radio.stop_scanning_networks()

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4) * 1000))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)
data = {}
response = None
print("Fetching json from", DRIVE_URL)
response = requests.get(DRIVE_URL)
print("-" * 40)
print(response.json())
print("-" * 40)
print("done")
# Read Response's HTTP status code
print("Response HTTP Status Code: ", response.status_code)
print("-" * 60)
# Close, delete and collect the response data
response.close()

myobj = {"somekey": "somevalue"}
x = requests.post(DRIVE_URL, json=myobj)
print(x.text)
