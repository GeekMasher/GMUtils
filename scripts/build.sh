#!/bin/bash

python3 setup.py install

echo "========================================================"
echo "    Testing..."
echo "========================================================"

python3 -m unittest discover -s 'tests' -p "test_*.py"
