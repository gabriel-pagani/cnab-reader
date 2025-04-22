from src.controller.cnab import Cnab
from time import sleep
from random import random

if __name__ == "__main__":
    sleep(random())
    cnab = Cnab()
    cnab.monitor()
