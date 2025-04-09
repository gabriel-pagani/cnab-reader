from src.utils.formatting import cnpj_format, date_format, value_format
from src.utils.connection import server_request, close_connection
from logging import error


class Cnab:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self.read()

    def read(self):
        """Read the CNAB file content"""
        try:
            with open(self.file_path, 'r', encoding='latin-1') as file:
                content = file.readlines()
            return content
        except Exception as e:
            error(f"Erro para ler o arquivo: {e}")

    def process(self):
        """Process the CNAB content and insert into database"""
        try:
            for row in self.content:
                if row[13] == 'E':
                    server_request(
                        query='insert into tcnab (colcnpj, banco, convenio, agencia, conta, datalan, valorlan, tipolan, desclan) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        params=(
                            cnpj_format(row[18:32]),      # Cnpj
                            row[0:3],                     # Banco
                            row[32:52],                   # Convênio
                            row[52:57],                   # Agência
                            row[58:70],                   # Conta
                            date_format(row[142:150]),    # Data Lançamento
                            value_format(row[150:168]),   # Valor Lançamento
                            row[168],                     # Tipo Lançamento
                            row[176:201].lower().strip()  # Descrição
                        )
                    )
                    close_connection()
        except Exception as e:
            error(f"Erro para inserir os dados na tabela: {e}")
            close_connection()
