from src.utils.connection import close_connection
from src.controller.cnab import Cnab
from time import sleep
from random import random

if __name__ == "__main__":
    try:
        sleep(random())
        cnab = Cnab()
        cnab.monitor()
    finally:
        close_connection()
