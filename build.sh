#!/bin/bash

python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install numpy
#pip3 install -r requirements.txt
apt-get install libgeos-dev
pip install https://github.com/matplotlib/basemap/archive/master.zip

deactivate
