import os
from time import sleep

from loguru import logger

from cartographer import Cartographer

TRAIL_COUNT = int(os.getenv("TRAIL_COUNT"))


def main():
    with Cartographer(TRAIL_COUNT) as cartographer:
        while True:
            cartographer.tend_trails()
            sleep(1)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as error:
            logger.info(f"Cartographer crashed, restarting: {str(error)}")
