# Carregador de Arquivos

Este projeto foi desenvolvido para prevenir problemas de qualidade de dados em dashboards e pipelines que dependem de arquivos carregados por analistas de negócios. Ele utiliza Streamlit para oferecer uma interface de usuário intuitiva para upload de arquivos e automaticamente valida se os arquivos carregados estão em conformidade com os formatos esperados pelos sistemas downstream. Também utiliza Databricks para armazenar os arquivos em um volume.

## Configuração do Ambiente

1. Criar um ambiente virtual: `python3 -m venv .venv`
2. Ativar o ambiente virtual: `source .venv/bin/activate`
3. Instalar as dependências: `pip install -r requirements.txt`

## Estrutura do Projeto e Variáveis / Parâmetros para Editar

### app.py

Este arquivo é responsável por construir a interface do usuário que permite o upload de arquivos.

### files.py

Define a estrutura dos arquivos de carga fria (schema, nome do volume, etc.).

1. files (linha 3): Configurar schemas e nomes dos arquivos que chegam via carga fria.

### uploader.py

Responsável por mover arquivos que estão em conformidade com a estrutura esperada para um Volume no workspace do Databricks.

1. **WorkspaceClient() (linha 6)**: Para testar localmente, você precisa configurar o perfil do workspace a ser usado.

    a. `databricks auth login` => Registra o perfil na sua máquina.

    b. `WorkspaceClient(profile="<nome do perfil>")` => Permite conectar ao workspace usando suas credenciais. Quando o app é implantado no Databricks, isso não é necessário. O app herda as autorizações do usuário.

2. **catalog, schema, e volume_name (linhas 8, 9 e 10)**: Devem apontar para o volume que foi criado no workspace.
