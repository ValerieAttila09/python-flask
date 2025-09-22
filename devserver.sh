#!/bin/sh
source .venv/bin/activate
python -u -m flask --app run run -p ${PORT:-5000} --debug
