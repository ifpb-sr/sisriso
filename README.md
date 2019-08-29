# sisriso

Descrição do propósito

# Desenvolvimento


Para utilizar o sisriso faz-se necessário configurar algumas variáveis de ambiente. Crie o arquivo `.env` com os valores apropriados, utilizando o arquivo `.env.exemplo` como base:

    cp .env.exemplo .env
    

# Testar HTML com templates

## Pré-requisitos
    * repositório baixado
        $ git clone https://github.com/ifpb-sr/sisriso.git
    * estar na pasta do repositório
        $ cd sisriso/
    * pipenv instalado
        $ pip install pipenv
    * estar com o ambiente virtual do pipenv ativado
        $ pipenv shell
    * estar com as dependencias do pipenv instalado
        $ pipenv install
    
## Configurações
Coloque o caminho do arquivo HTML no return da sua rota

Caminho:
