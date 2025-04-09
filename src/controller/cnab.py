from src.utils.formatting import cnpj_format, date_format, value_format, code_format
from src.utils.connection import server_request, close_connection
from logging import error
from os import listdir, path


class Cnab:
    def __init__(self):
        self.folder_path = [
            r"\\192.168.42.153\Extratos\BRS Vias\Bradesco",
            r"\\192.168.42.153\Extratos\ICD\Bradesco",
            r"\\192.168.42.153\Extratos\ICD\UNICRED",
            r"\\192.168.42.153\Extratos\Sinasc Construcao\Bradesco",
            r"\\192.168.42.153\Extratos\Sinasc Construcao\BS2",
            r"\\192.168.42.153\Extratos\Sinasc Construcao\Santander",
            r"\\192.168.42.153\Extratos\Sinasc Construcao\Sicoob",
        ]

    @staticmethod
    def read(file_path: str) -> list:
        """Read the CNAB file content"""
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.readlines()
            return content
        except Exception as e:
            error(f"Erro ao ler o arquivo: {e}")

    @staticmethod
    def process(content: list) -> None:
        """Process the CNAB content and insert into database"""
        try:
            for row in content:
                if row[7] in ['1', '3', '5']:
                    desc = None if row[7] != '3' else row[176:201].lower(
                    ).strip()

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
                            desc,                          # Descrição
                            row[7]                         # Tipo Registro
                        )
                    )
                    close_connection()
        except Exception as e:
            error(f"Erro ao inserir os dados na tabela: {e}")
            close_connection()

    def monitor(self):
        """Monitora continuamente as pastas em busca de novos arquivos .ret"""
        try:
            while True:
                for folder in self.folder_path:
                    files = listdir(folder)
                    for file in files:
                        if file.lower().endswith('.ret'):
                            file_path = path.join(folder, file)
                            Cnab.process(Cnab.read(file_path))

                break
        except Exception as e:
            error(f"Erro durante o monitoramento: {e}")
