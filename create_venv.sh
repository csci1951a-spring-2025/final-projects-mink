#!/bin/bash

# this installs the virtualenv module
python3.11 -m pip install virtualenv
# this cd to your root directory and install a virtual environment named cs1951a_venv
cd
python3.11 -m venv cs1951a_venv
dir=$(pwd)
# activate the created virtual environment
source cs1951a_venv/bin/activate
# go back to the previous directory
cd -
# and copy requirements.txt to the venv directory
cp requirements.txt ~/cs1951a_venv/.
# and then cd back to the venv
cd "$dir/cs1951a_venv/"
# and then the real pip here is the bin/pip
pip_env=$dir/cs1951a_venv/bin/pip
python_env=$dir/cs1951a_venv/bin/python3
# update pip
$pip_env install -U pip
# then write to ~/.bashrc and ~/.bash_profile that cs1951a_venv from now on is to activate the
# virtual environment
$python_env -m pip install -r requirements.txt

echo created cs1951a environment
# now go back to the previous directory
cd -