#!/bin/bash

echo "Starting mongodb"
/opt/mongodb/bin/mongod --dbpath /opt/mongo-data > /opt/logs/mongo.log 2>&1 &

echo "Starting Server"
python ${ARTSPEAKER_DEV}/server/views.py > /opt/logs/server.log 2>&1 &
echo "Starting Client"
python ${ARTSPEAKER_DEV}/client/views.py > /opt/logs/client.log 2>&1 &
echo "Done. Waiting..."

wait