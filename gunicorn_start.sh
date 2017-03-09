#!/bin/bash

NAME=myhome
DJANGODIR=/home/pi/myhome/mysite
APP=mysite.wsgi
SOCKFILE=gunicorn.sock
RUNAS=root
NUM_WORKERS=2

cd $DJANGODIR
source ../venv/bin/activate

PATH=$PATH:../433Utils/RPi_utils

exec ../venv/bin/gunicorn $APP \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user $RUNAS  \
    --bind=unix:$SOCKFILE \
    --log-level=DEBUG \
    --log-file=../logs/gunicorn.log \
    --capture-output

