#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/hello.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=webserver
GROUP=serveruser
cd /home/ubuntu/server_env/speedbarter
source ../bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec ../bin/gunicorn speedbarter.wsgi:application -w $NUM_WORKERS
    --user=$USER --group=$GROUP --log-level=debug
    --log-file=$LOGFILE 2>>$LOGFILE