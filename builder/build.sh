#!/bin/bash

set -e

curl https://publicsuffix.org/list/public_suffix_list.dat | sed '/^$/d' | grep -v -- "//" > files/list.dat
python builder/to_pickle.py
