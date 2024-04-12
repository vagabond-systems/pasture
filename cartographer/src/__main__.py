from time import sleep

from cartographer import Cartographer

with Cartographer(3) as cartographer:
    while True:
        cartographer.tend_trails()
        sleep(1)
