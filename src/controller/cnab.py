from src.utils.formatting import cnpj_format, date_format, value_format, code_format
from src.utils.connection import server_request, close_connection
from logging import error
from os import listdir, path, system
from time import sleep
from threading import Thread


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
    def process(content: list, file: str) -> None:
        """Process the CNAB content and insert into database"""
        try:
            for row in content:

                cnpj = row[18:32]
                banco = row[0:3]
                convenio = row[32:52]
                agencia = row[52:57]
                conta = row[58:70]
                data = row[142:150]
                valor = row[150:168]
                tipo = row[168]
                desc = row[176:201].upper() if row[7] == '3' else None
                tipo_registro = row[7]

                if tipo_registro in ['1', '3', '5']:
                    server_request(
                        query='insert into zcnab (colcnpj, banco, convenio, agencia, conta, datalan, valorlan, tipolan, desclan, tiporegis, arquivo_importado) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        params=(
                            cnpj_format(cnpj),
                            banco,
                            code_format(convenio),
                            code_format(agencia),
                            code_format(conta),
                            date_format(data),
                            value_format(valor),
                            tipo,
                            desc,
                            tipo_registro,
                            file
                        )
                    )
                    close_connection()
        except Exception as e:
            error(f"Erro ao inserir os dados na tabela: {e}")
            close_connection()

    def message(self):
        """Thread para mostrar a mensagem de monitoramento com animação"""
        msgs = ['Monitorando diretórios.',
                'Monitorando diretórios..',
                'Monitorando diretórios...']
        while True:
            for msg in msgs:
                system('cls')
                print(msg)
                sleep(0.5)

    def monitor(self):
        """Monitora continuamente as pastas em busca de novos arquivos .ret"""
        Thread(target=self.message, daemon=True).start()
        try:
            while True:
                for folder in self.folder_path:
                    files = listdir(folder)
                    for file in files:
                        response = server_request(
                            query="select id from zcnab where arquivo_importado = ?",
                            params=(file)
                        )
                        if file.lower().endswith('.ret') and response['data'] == []:
                            file_path = path.join(folder, file)
                            Cnab.process(Cnab.read(file_path), file)

        except Exception as e:
            error(f"Erro durante o monitoramento: {e}")
