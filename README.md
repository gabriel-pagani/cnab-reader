# Descrição
Esse sistema foi desenvolvido com o objetivo de automatizar a inserção de dados bancários no banco de dados

# Pré-requisitos
- Python 3.13+
- Windows 11
- SQL Server 18+

# Instalação
- Clone o repositório
```bash
git clone https://github.com/gabriel-pagani/cnab-reader.git
```
- Entre na pasta clonada
```powershell
cd cnab-reader
```
- Crie um ambiente virtual
```powershell
python -m venv venv
```
- Ative o ambiente virtual
```powershell
venv\Scripts\activate
```
- Instale as dependências
```powershell
pip install -r requirements.txt
```

# Configuração
Na pasta cnab-reader crie o ".env". Dentro do arquivo ".env" adicione o seguinte conteúdo
```
SERVER=endereco_do_seu_servidor
DATABASE=nome_da_sua_base_de_dados
USER=seu_usuario
PASSWORD=sua_senha
```

Dentro do seu gerenciador do banco de dados execulte o seguinte script
- [Tabela](https://github.com/gabriel-pagani/cnab-reader/blob/main/data/script_database.sql)

# Estrutura do Projeto
```
projeto/
├── data/               # Script do banco de dados
├── src/                # Código fonte
├── venv/               # Configurações do ambiente virtual
├── .env                # Arquivo de configuração de ambiente
├── .gitignore          # Especifica arquivos a serem ignorados pelo git
├── LICENSE             # Arquivo de licença do projeto
├── main.py             # Arquivo principal de execução
├── README.md           # Este arquivo
└── requirements.txt    # Lista de dependências do projeto
```

# Mode de Uso
- Execulte o arquivo main.py
```powershell
python main.py
```

# Licença 
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/gabriel-pagani/cnab-reader/blob/main/LICENSE) para mais detalhes. A Licença MIT é uma licença de software livre que permite o uso, cópia, modificação e distribuição do código, desde que incluída a nota de direitos autorais e a permissão original.

# Contato 
Email - gabrielpaganidesouza@gmail.com