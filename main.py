from src.utils.connection import close_connection
from src.controller.cnab import Cnab


if __name__ == "__main__":
    try:
        processor = Cnab()
        processor.process()
    finally:
        close_connection()
