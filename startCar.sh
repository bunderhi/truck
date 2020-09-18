#! /usr/bin/bash

function startCar() {
    python manage.py drive >/tmp/dc/car.log 2>/tmp/dc/error.log &
}
echo $(startCar()) > /tmp/dc/carPID


if ps -p $carPID > /dev/null
then
    echo "Running"
fi

