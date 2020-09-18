#! /usr/bin/bash

function startCar() {
    python manage.py drive &
}
cd /home/brian/mycar
echo $(startCar()) > /tmp/dc/carPID