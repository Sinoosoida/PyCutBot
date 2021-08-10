#!/bin/bash
apt update
apt install python3-pip
pip3 install -r requirements.txt
apt install ffmpeg
python3 -m pip install -e .
echo "DONE"