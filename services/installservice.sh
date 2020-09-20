sudo cp /home/projects/truck/services/startcar.service /etc/systemd/system/startcar.service
#
#Add the rule (file 99-local.rules) to start system unit service when ttyUSB0 is available
sudo cp  /homels/projects/truck/services/99-startcar.rules /etc/udev/rules.d/99-startcar.rules
#
sudo udevadm control -l debug           #allows debugging (tail –f /var/log/syslog)
sudo udevadm control --reload-rules     #reloads rules
sudo systemctl daemon-reload            #reloads systemd