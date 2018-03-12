#!/bin/bash

python3 setup.py install
RESULT=$?

function banner {
    echo "========================================================"
    echo "    $1..."
    echo "========================================================"
}


if [ $RESULT == 0 ]; then
    banner 'Testing'

    python3 -m unittest discover -s 'tests' -p "test_*.py"
    RESULT=$?
fi

if [ $RESULT == 0 ]; then
    banner 'Coverage'

    coverage run --source=src/gmutils -m unittest discover -s 'tests' -p "test_*.py"
    RESULT=$?
fi

if [ $RESULT == 0 ]; then
    banner 'Documentation'

    sphinx-build -b html docs/ docs/_build && rm -r docs/_build/.doctrees
    RESULT=$?
fi
