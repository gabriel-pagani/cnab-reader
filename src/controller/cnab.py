from src.utils.formatting import cnpj_format, date_format, value_format, code_format
from src.utils.connection import server_request, close_connection
from logging import error


class Cnab:
    def __init__(self):
        self.file_path = r'\\192.168.42.153\Extratos\Sinasc Construcao\Bradesco\EXT_237_94959_250403_00000.RET'
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
                if row[7] == '1':
                    server_request(
                        query='insert into zcnab (colcnpj, banco, convenio, agencia, conta, datalan, valorlan, tipolan, desclan, tiporegis) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        params=(
                            cnpj_format(row[18:32]),       # Cnpj
                            row[0:3],                      # Banco
                            code_format(row[32:52]),       # Convênio
                            code_format(row[52:57]),       # Agência
                            code_format(row[58:70]),       # Conta
                            date_format(row[142:150]),     # Data Lançamento
                            value_format(row[150:168]),    # Valor Lançamento
                            row[168],                      # Tipo Lançamento
                            '',                            # Descrição
                            '1'                            # Tipo Registro
                        )
                    )
                    close_connection()
                if row[7] == '3':
                    server_request(
                        query='insert into zcnab (colcnpj, banco, convenio, agencia, conta, datalan, valorlan, tipolan, desclan, tiporegis) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        params=(
                            cnpj_format(row[18:32]),       # Cnpj
                            row[0:3],                      # Banco
                            code_format(row[32:52]),       # Convênio
                            code_format(row[52:57]),       # Agência
                            code_format(row[58:70]),       # Conta
                            date_format(row[142:150]),     # Data Lançamento
                            value_format(row[150:168]),    # Valor Lançamento
                            row[168],                      # Tipo Lançamento
                            row[176:201].lower().strip(),  # Descrição
                            '3'                            # Tipo Registro
                        )
                    )
                    close_connection()
                if row[7] == '5':
                    server_request(
                        query='insert into zcnab (colcnpj, banco, convenio, agencia, conta, datalan, valorlan, tipolan, desclan, tiporegis) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        params=(
                            cnpj_format(row[18:32]),       # Cnpj
                            row[0:3],                      # Banco
                            code_format(row[32:52]),       # Convênio
                            code_format(row[52:57]),       # Agência
                            code_format(row[58:70]),       # Conta
                            date_format(row[142:150]),     # Data Lançamento
                            value_format(row[150:168]),    # Valor Lançamento
                            row[168],                      # Tipo Lançamento
                            '',                            # Descrição
                            '5'                            # Tipo Registro
                        )
                    )
                    close_connection()
        except Exception as e:
            error(f"Erro para inserir os dados na tabela: {e}")
            close_connection()
