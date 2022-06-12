# Luizalabs API Case

## Cenário Proposto
Prover 3 serviços relativos ao envio de comunicação da empresa, esses devem consistir em:
  - Agendamento do envio da comunicação;
  - Consulta do envio da comunicação;
  - Cancelamento do envio da comunicação

## Solução
### **1 - Criação do Banco de Dados Relacional**
O primeiro passo para o desenvolvimento do projeto consistiu na definição do schema do banco de dados relacional, nesse caso optou-se pela criação de uma entidade no MySql.

A tabela denominada "agendamento" consiste no agrupamento das features:
  - id_agendamento: ID único atribuído a cada agendamento (int)
  - id_usuario: ID atribuído ao usuário que receberá a comunicação (int)
  - dt_envio: Data programada para o envio da comunicação (datetime)
  - formato_comunicacao: e-mail, sms, push, whatsapp (str)
  - status_agendamento: Enviado, Cancelado, Agendado (str)
  - dt_atualizacao: Data da última atualização do registro no banco (datetime)

A partir das features apresentadas acima, acredita-se que as possíveis aplicações que consumirão os serviços disponibilizados estarão servidas com as informações necessárias.

### **2 - Desenvolvimento do Endpoint de Ingestão de Dados**
O primeiro serviço desenvolvido foi o endpoint de ingestão de dados.
Consiste na utilização do método POST no endpoint "/agendamento", para tal, espera-se receber os campos obrigatórios em formato json, como especificado no exemplo abaixo:

{
    "id_agendamento": 1,
    "id_usuario": 11,
    "dt_envio": "2022/12/11 12:00:00",
    "formato_comunicacao": "Whatsapp"
}

Como esse processo é o primeiro da cadeia, atribuiu-se valores defaualt para os seguintes campos:
  - status_agendamento: "agendado"
  - dt_atualizacao: data de inserção no banco


### **3 - Desenvolvimento do Endpoint de Consulta de Dados**
O segundo endpoint desenvolvido utiliza o método GET no endpoint "/status/<id_agendamento>".
Para a consulta dos dados de um registro no banco de dados, deve-se passar como parâmetro da requisição o ID único atribuído a cada agendamento.

### **4 - Desenvolvimento do Endpoint de Atualização de Dados**
Já o último endpoint desenvolvido consiste na atualização do campo "status_agendamento" no banco de dados.
Assim, os consumidores do serviço podem atualizar o banco de dados e cancelar um agendamento de envio.
Para isso utiliza-se o método PATCH no endpoint "/cancelamento/id_agendamento>", deve-se passar como parâmetro da requisição o ID único atribuído a cada agendamento.
Além disso, espera-se um json no seguinte formato:

{
    "status_agendamento": "cancelado"
}

## Reprodução do Projeto
Para reproduzir o projeto em ambiente Linux:
  - Clone o repositório;
  - Garanta que o MySQL server esteja rodando;
  - Execute o script [main.py](https://github.com/willytakasawa/dev-api-case/blob/master/main.py), esse script é responsável pela criação do banco de dados e da tabela     agendamento com todos as constraints definidas, além disso, a aplicação estará disponinível em localhost "http://localhost:5000";
  - Execute o script [test_default.py](https://github.com/willytakasawa/dev-api-case/blob/master/test_default.py). Para garantir que a aplicação está funcionando,         funcionando sem erros, criou-se um script para execução de testes unitários, para isso, execute no terminal o comando: py.test
    
    O resultado esperado será semelhante ao demonstrado abaixo:
    
    ![test_result](https://github.com/willytakasawa/dev-api-case/blob/master/raw_pic/test_result.png)
