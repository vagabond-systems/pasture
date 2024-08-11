from time import sleep

from loguru import logger

from shepherd import Shepherd


def main():
    with Shepherd() as shepherd:
        while True:
            shepherd.tend()
            sleep(0.3)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as error:
            logger.info(f"Shepherd crashed, restarting: {str(error)}")
            sleep(0.3)
