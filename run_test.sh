#!/bin/bash

BASE_PORT=16998
INCREMENT=1

port=$BASE_PORT
isfree=$(netstat -taln | grep $port)

while [[ -n "$isfree" ]]; do
    port=$[port+INCREMENT]
    isfree=$(netstat -taln | grep $port)
done

export DB_PORT=$port
python prepare_testenv.py
echo "use port number $port as database port for testing"
sleep 5
python -m unittest -v
python shutdown_env.py
unset DB_PORT