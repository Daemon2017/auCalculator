#!/bin/sh
apt-get update
apt-get install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install build-essential -y
apt-get install python3.8-distutils -y
apt-get install python3.8 -y
apt-get install python3-pip -y
apt-get install python3-markupsafe -y
python3.8 -m pip install -r requirements.txt
