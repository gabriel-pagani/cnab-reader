from src.utils.connection import close_connection
from src.controller.cnab import Cnab

if __name__ == "__main__":
    try:
        cnab = Cnab()
        cnab.monitor()
    finally:
        close_connection()
