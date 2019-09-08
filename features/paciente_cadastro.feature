# – FILE: features/usuario_cadastro.feature # language: pt
Funcionalidade: Cadastro do paciente

Para que eu possa seja atendido
Como um Paciente
Eu quero ser registrado no sistema

Fundo:
  Dado um paciente registrado:
  |nome    |tipoSanguinio|idade|sexo|rg     |cpf        |profissao|indicacao |
  |Jean-Luc|A+           |17   |M   |4852258|12345678900|Capitão  |James Kirk|
  E com as informações de endereco preenchidas
  |tipo|logradouro|numero|bairro |cidade    |estado|cep      |
  |rua |Para      |59    |popular|Santa Rita|PB    |58000-300|
  E com as informações de urgencia preenchidas
  |urgenciaNome |urgenciaTelefone|observacao|
  |William Riker|83988776655     |Primo     |
  E com as informações do convenio dado
  |matr|convenio_id|
  |0001|0001       |

Regra: O nome, tipoSanguinio, idade, sexo, rg, cpf, profissao e indicacao são obrigatórios no cadastro
  Exemplo: Falha no cadastro devido a ausência do nome
  Quando tentar cadastrar um paciente com os seguintes dados:
  |tipoSanguinio|idade|sexo|rg     |cpf        |profissao |indicacao  |
  |O+           |17   |M   |8569987|11122233344|Comandante|W. T. Riker|
  Então Será exibida uma mensagem informando que "nome" deve ser preenchido
