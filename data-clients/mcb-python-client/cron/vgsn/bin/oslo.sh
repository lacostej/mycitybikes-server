#!/bin/bash
export PATH=/usr/local/bin/:$PATH
PYTHONPATH=./src/:.:~/local/lib/python2.5/:/usr/local/lib/python python2.5 test/mycitybikes-oslo-clearchannel.py
