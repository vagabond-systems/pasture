import os
from time import sleep

from cartographer import Cartographer

TRAIL_COUNT = os.getenv("TRAIL_COUNT")

with Cartographer(TRAIL_COUNT) as cartographer:
    while True:
        cartographer.tend_trails()
        sleep(1)
