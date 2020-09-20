#! /bin/bash
VIRTUAL_ENV='/home/brian/env'
export VIRTUAL_ENV
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

cd /home/brian/mycar
python nextion_test.py 
