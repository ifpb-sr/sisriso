# sisriso

Auxliar na administração de um consultório de um dentista

## Funcionalidades

 Descrever funcionalidades

# Desenvolvimento


Para utilizar o sisriso faz-se necessário configurar algumas variáveis de ambiente. Crie o arquivo `.env` com os valores apropriados, utilizando o arquivo `.env.exemplo` como base:

    cp .env.exemplo .env
 
# Testar HTML com templates

## Pré-requisitos
* repositório baixado

~~~shell script
$ git clone https://github.com/ifpb-sr/sisriso.git
~~~
        
* estar na pasta do repositório

        $ cd sisriso/
        
* pipenv instalado

        $ pip install pipenv
        
* estar com o ambiente virtual do pipenv ativado

        $ pipenv shell
        
* estar com as dependencias do pipenv instalado

        $ pipenv install
    
## Configurando
### Arquivos
Coloque o arquivo HTML na pasta templates

> Se tiver uma pasta específica para sua página, coloque o seu arquivo lá

> OBS: O ideal é que as alterações sejam feitas ja dentro do repositório, caso não esteja fazendo isso e o seu arquivo ainda não existir no repositório crie ele e o adicione ao repositório, CASO JÁ ESTEJA TRABALHANDO ASSIM,*DESCONSIDERE*

![Exemplo da aparência da pasta `templates`](https://github.com/alefemoreira/imagens/blob/master/Captura%20de%20tela%20de%202019-09-04%2017-39-55.png)

### Variáveis de ambiente
Crie o arquivo `.env` com os valores apropriados, utilizando o arquivo `.env.exemplo` como base:

    cp .env.exemplo .env
    
Configure casa variável com os seguintes valores

    export FLASK_APP=app.py
    export FLASK_ENV=development

A variável `FLASK_ENV` configurada com esse valor ativa o modo debug e o `FLASK_APP` indica em que arquivo esta o programa com FLASK.

Para configurar as variáveis basta executar o seguinte comando
   
    $ source .env
    
### Rotas
Verifique se ja existe uma rota no arquivo `app.py` para sua página. Se existir, será parecido com a imagem a seguir:

![Exemplo de rota](https://github.com/alefemoreira/imagens/blob/master/Captura%20de%20tela%20de%202019-09-04%2018-10-54.png)

**Caso não exista basta copiar as linhas abaixo e alterar o que esta digitado da seguinte forma `ALGO_EM_MAIUSCULO`**

~~~python
@app.route('/NOME_DO_SEU_CAMINHO')
def NOME_DO_SEU_CAMINHO():
    return render_template('CAMINHO_DO_SEU_ARQUIVO')
#O caminho do arquivo é relativo a pasta templates
~~~

## Executando
Para executar verifique se estar com o `pipenv` está ativado. Se estiver o terminal terá o `(sisriso)` na frente na sua posição. CUIDADO PARA NÃO SAIR DA PASTA DO PROJETO COM ELE ATIVADO.

![Terminal com o pipenv ativo](https://github.com/alefemoreira/imagens/blob/master/Captura%20de%20tela%20de%202019-09-04%2018-18-26.png)

Agora basta executar o seguinte comando:

    flask run -p 8080

* Agora se você estiver na AWS, precisa executar os seguintes passos:

        Clicar em `preview` no menu do topo
        Em seguida clique em `Preview Running Application`
        Digite seu caminho na barra de pesquisa da janela que irá se abrir

![Menu do Topo](https://github.com/alefemoreira/imagens/blob/master/Captura%20de%20tela%20de%202019-09-04%2018-23-12.png)
![Janela Que Se Abre](https://github.com/alefemoreira/imagens/blob/master/Captura%20de%20tela%20de%202019-09-04%2018-27-28.png)

* Agora se você estiver em um computador, basta abrir um navegador e digitar o link:

        localhost:8080/$NOME_DO_SEU_CAMINHO

# License
Esse sistema é disponibilizado como software livre através da [Licença MIT](http://opensource.org/licenses/MIT).
