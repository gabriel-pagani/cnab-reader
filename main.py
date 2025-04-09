from src.utils.connection import close_connection
from src.controller.cnab import monitor_folders


if __name__ == "__main__":
    try:
        monitor_folders()
    finally:
        close_connection()
