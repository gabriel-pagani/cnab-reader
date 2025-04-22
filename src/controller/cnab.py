from src.utils.formatting import cnpj_format, date_format, value_format, code_format
from src.utils.connection import server_request
from logging import error
from os import listdir, path
from dotenv import load_dotenv
from os import getenv
from threading import Thread


load_dotenv()


class Cnab:
    def __init__(self):
        self.folder_path = getenv("FOLDER_PATH").split(",")

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
                desc = row[176:201].upper(
                ) if row[7] == '3' and not row[176:201].isspace() else None
                tipo_registro = row[7]

                if tipo_registro in ['1', '3', '5']:
                    server_request(
                        query='insert into zcnab (colcnpj, banco, convenio, agencia, conta, datalan, valorlan, tipolan, desclan, tiporegis, arqvimport) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
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
        except Exception as e:
            error(f"Erro ao inserir os dados na tabela: {e}")

    def counter(self) -> None:
        """Conta o número total de registros do tipo 1, 3 ou 5 em todos os arquivos"""
        count = 0
        for folder in self.folder_path:
            for file in listdir(folder):
                if file.lower().endswith('.ret'):
                    file_path = path.join(folder, file)
                    content = Cnab.read(file_path)
                    for row in content:
                        if row[7] in ['1', '3', '5']:
                            count += 1
        print(count)

    def monitor_folder(self, folder):
        """Monitora continuamente as pastas em busca de novos arquivos .ret"""
        try:
            for file in listdir(folder):
                if file.lower().endswith('.ret'):
                    response = server_request(
                        query="select id from zcnab where arqvimport = ?",
                        params=(file)
                    )
                    if response['data'] == []:
                        file_path = path.join(folder, file)
                        Cnab.process(Cnab.read(file_path), file)
        except Exception as e:
            error(f"Erro durante o monitoramento da pasta {folder}: {e}")

    def monitor(self):
        """Cria threads para monitorar múltiplas pastas paralelamente"""
        threads = []
        for folder in self.folder_path:
            t = Thread(target=self.monitor_folder, args=(folder.strip(),))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
