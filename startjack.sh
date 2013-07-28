#!/usr/bin/env bash

nohup jackd -d alsa &
sleep 0.2
nohup jack-keyboard & 
nohup calfjackhost organ ! & 
nohup a2jmidid &
sleep 2

./touch.py $1 $2 $3 $4
