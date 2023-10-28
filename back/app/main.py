import sys

from loguru import logger

logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])


def main():
    logger.info("HI")
    logger.error("BYE")


if __name__ == "__main__":
    main()
