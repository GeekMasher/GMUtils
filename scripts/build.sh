#!/bin/bash

python3 setup.py install
RESULT=$?


if [ $RESULT == 0 ]; then
    echo "========================================================"
    echo "    Testing..."
    echo "========================================================"

    python3 -m unittest discover -s 'tests' -p "test_*.py"
    RESULT=$?
fi


if [ $RESULT == 0 ]; then
    echo "========================================================"
    echo "    Documentation..."
    echo "========================================================"

    sphinx-build -b html docs/ docs/_build && rm -r docs/_build/.doctrees
    RESULT=$?
fi
