#!/bin/bash

echo "Starting mongodb"
/opt/mongodb/bin/mongod --smallfiles --dbpath /opt/mongo-data > /var/log/artspeaker/mongo.log 2>&1 &

echo "Starting Server"
python ${ARTSPEAKER_DEV}/server/views.py > /var/log/artspeaker/server.log 2>&1 &
echo "Starting Client"
python ${ARTSPEAKER_DEV}/client/views.py > /var/log/artspeaker/client.log 2>&1 &
echo "Done. Waiting..."

wait
