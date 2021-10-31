# CRManager
Gerenciador de processos e registros pessoais do Departamento de Fiscalização de Produtos Controlados.

## Descrição
Este projeto tem como objetivo ser o backend, implementado em Django 3.x, do projeto de gerenciador pessoal de processos e registros do Departamento de Fiscalização de Produtos Controlados (DFPC) do Exército Brasileiro, tanto aqueles processos criados via SisGCorp quanto os processos criados via pasta física diretamente na Secretaria de Fiscalização de Produtos Controlados (SFPC) da região do usuário.

Esta ferramenta se destina aos usuários e despachantes que precisam gerenciar seus processos de forma simples através de um aplicativo Android (infelizmente iOS não será possível, visto que não possuo dispositivos para o desenvolvimento) que em breve será desenvolvido e o link do projeto incluído aqui (não haverá disponibilidade no Google Play).

Os processos que podem ser gerenciados inicialmente são:
- Concessão de CR
- Atualização de Endereço do Acervo
- Atualização de Documento Pessoal
- Atualização de Tipo de Atividade
- Cancelamento de CR para Pessoa Física
- Inclusão de 2º Endereço de Acervo
- Autorização de Compra
- CRAF
- Guia de Trânsito
- Apostilamento
- Autorização de Aquisição de PCE por Importação (CII)
- Instituir Procurador para Pessoa Física
- Revalidação para Pessoa Física

É possível também criar um perfil de usuário com as informações úteis da pessoa física, como E-Mail, CPF, RG, data de nascimento e endereços de acervo (principal e segundo endereço).

Também é possível registrar um CR para o usuário, o que auxilia no gerenciamento das atividades permitidas vinculadas ao documento.

Através dessa ferramenta, é possível cadastrar todos os processos pendentes ou já concluídos do usuário, com informações detalhadas sobre os processos e com a contagem de dias úteis e dias corridos desde o início do processo e da compensação da GRU.

Abaixo está alguns prints do painel de controle do projeto:

**Gerenciador de Processos:**
<img src="https://github.com/Wolfterro/CRManager/raw/master/docs/screenshots/screnshot1.png" />

**Gerenciador de Perfil de Usuários:**
<img src="https://github.com/Wolfterro/CRManager/raw/master/docs/screenshots/screnshot2.png" />

**Gerenciador de CR:**
<img src="https://github.com/Wolfterro/CRManager/raw/master/docs/screenshots/screnshot3.png" />

## Instalação
Para a instalação o projeto recomenda-se criar primeiro uma virtualenv:
```shell
$ mkvirtualenv CRManager --python=python3
```

Após a criação da virtualenv e certificar-se de que está acessando a virtualenv, rode o seguinte comando:
```shell
(CRManager) $ make install
```

Durante o processo de instalação, será requisitado que você crie uma conta de super usuário, para acessar o painel via endereço ```https://localhost:8000/admin```. 


Sempre que quiser rodar o projeto, basta usar o comando ```make run```:
```shell
(CRManager) $ make run
```

## Collection
A collection deste backend pode ser encontrada aqui: https://www.getpostman.com/collections/54722ca1478e12ca4109
