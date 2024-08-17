#!/bin/bash

. ../../.venv/bin/activate
python3 setup.py sdist
twine upload --skip-existing dist/* --non-interactive
