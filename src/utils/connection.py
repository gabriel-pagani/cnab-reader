from pyodbc import connect, Error
from os import getenv
from dotenv import load_dotenv
from logging import error, basicConfig, ERROR


load_dotenv()
_connection = None
basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
            filename='main.log', level=ERROR)


def get_connection() -> connect:
    global _connection
    if _connection is None or _connection.closed:
        server_connection = f'DRIVER={{SQL Server}}; SERVER={getenv("SERVER")}; DATABASE={getenv("DATABASE")}; UID={getenv("USER")}; PWD={getenv("PASSWORD")}'
        try:
            _connection = connect(server_connection)
        except Error as e:
            error(f"Erro ao conectar ao banco de dados: {e}")
            raise
    return _connection


def server_request(query: str, params: tuple = None) -> dict:
    response = dict()

    try:
        connection = get_connection()
        with connection.cursor() as cursor:

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.lower().strip().startswith('select'):
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()

                result = []
                for row in data:
                    result.append(dict(zip(columns, row)))

                response['data'] = result
            else:
                connection.commit()

    except Error as e:
        error(f"Erro de banco de dados: {e}")

    except Exception as e:
        error(f"Erro inesperado: {e}")

    return response


def close_connection():
    global _connection
    if _connection and not _connection.closed:
        _connection.close()
        _connection = None
