#! /usr/bin/bash

function startCar() {
    python manage.py drive &
}
echo $(startCar()) > /tmp/dc/carPID