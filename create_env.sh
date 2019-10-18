#! /bin/bash

python3 -m venv temp_env

source ./temp_env/bin/activate

pip3 install tweety pandas matplotlib numpy

pip3 freeze > reqs.txt

deactivate

