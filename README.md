# 📊 Sistema de Gerenciamento de Produtos e Usuários

![Licença](https://img.shields.io/badge/Licença-MIT-green)
![Versão](https://img.shields.io/badge/Versão-1.0-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📝 Relatório Técnico

Este documento apresenta o relatório técnico do desenvolvimento do Sistema de Gerenciamento de Produtos e Usuários, uma aplicação web construída seguindo o padrão de arquitetura MVC (Model-View-Controller).

---

## 📋 Sumário

1. [📌 Visão Geral](#-visão-geral)
2. [🏗️ Arquitetura MVC](#️-arquitetura-mvc)
3. [🔧 Tecnologias Utilizadas](#-tecnologias-utilizadas)
4. [⚙️ Implementação](#️-implementação)
5. [✅ Validação de Campos](#-validação-de-campos)
6. [🚧 Desafios e Soluções](#-desafios-e-soluções)
7. [🚀 Como Executar](#-como-executar)
8. [🔌 Endpoints da API](#-endpoints-da-api)
9. [📚 Referências](#-referências)

---

## 📌 Visão Geral

O Sistema de Gerenciamento de Produtos e Usuários é uma aplicação web desenvolvida para gerenciar o cadastro, visualização, edição e remoção de produtos e usuários. A aplicação oferece uma API RESTful com endpoints bem definidos, além de uma interface de usuário para interação com o sistema.

---

## 🏗️ Arquitetura MVC

A aplicação foi desenvolvida seguindo o padrão de arquitetura MVC (Model-View-Controller), que separa a aplicação em três componentes principais:

### 📦 Model

Os modelos representam a estrutura de dados da aplicação. Eles são responsáveis por:
- Definir a estrutura das entidades (produtos e usuários)
- Interagir com o banco de dados

### 🖼️ View

As views são responsáveis pela apresentação dos dados ao usuário. No nosso sistema, utilizamos:
- Templates HTML para renderizar páginas
- CSS para estilização de elementos
- Formulários para entrada de dados

### 🎮 Controller

Os controllers gerenciam o fluxo da aplicação, processando requisições, interagindo com os modelos e retornando respostas:

## 🔧 Tecnologias Utilizadas

| Categoria | Tecnologia |
|-----------|------------|
| **Backend** | Python com FastAPI |
| **Banco de Dados** | MySQL - Sistema de gerenciamento de banco de dados |
| **Frontend** | HTML e CSS para interface do usuário |
| **Validação** | Pydantic - Biblioteca Python para validação de dados |

---

## ⚙️ Implementação

### 📂 Estrutura do Projeto

A estrutura do projeto segue a arquitetura MVC, com separação clara de responsabilidades entre os diferentes componentes:

```
FASTAPI_P1-MAIN/
├── controllers/                # Controladores da aplicação
│   ├── produto_controller.py   # Controlador de produtos
│   └── usuario_controller.py   # Controlador de usuários
├── database/                   # Configuração do banco de dados
│   └── config.py               # Configurações de conexão
├── models/                     # Modelos da aplicação
│   ├── database.py             # Configuração do ORM
│   ├── produto_model.py        # Modelo de produtos
│   └── usuario_model.py        # Modelo de usuários
├── routes/                     # Rotas da API
│   ├── produtos_routes.py      # Rotas de produtos
│   └── usuario_routes.py       # Rotas de usuários
├── templates/                  # Templates HTML
│   ├── produtos/               # Templates relacionados a produtos
│   │   ├── cadastro.html       # Formulário de cadastro de produtos
│   │   ├── detalhes.html       # Página de detalhes do produto
│   │   ├── editar.html         # Formulário de edição de produtos
│   │   └── lista.html          # Lista de produtos
│   ├── usuarios/               # Templates relacionados a usuários
│   │   ├── cadastro.html       # Formulário de cadastro de usuários
│   │   ├── detalhes.html       # Página de detalhes do usuário
│   │   ├── editar.html         # Formulário de edição de usuários
│   │   └── lista.html          # Lista de usuários
│   ├── base.html               # Template base para herança
│   └── index.html              # Página inicial
├── validators/                 # Validadores de dados
│   ├── produto_validator.py    # Validação de produtos
│   └── usuario_validator.py    # Validação de usuários
├── .env.example                # Exemplo de variáveis de ambiente
├── main.py                     # Ponto de entrada da aplicação
├── README.md                   # Documentação do projeto
└── requirements.txt            # Dependências do projeto
```

### 🔄 Fluxo da Aplicação

1. O usuário acessa uma URL
2. O router direciona a requisição para o controller apropriado
3. O controller processa a requisição e interage com os modelos necessários
4. Os dados são validados antes de serem processados
5. O resultado é renderizado em um template ou retornado como resposta

---

## ✅ Validação de Campos

A validação de campos é um aspecto crucial da aplicação, garantindo que apenas dados válidos sejam processados:

- **🔤 Validação de Tipos**: Garantir que os dados estejam no formato correto
- **📏 Validação de Restrições**: Verificar comprimentos mínimos/máximos, valores permitidos
  

## 🚧 Desafios e Soluções

### 🔒 Segurança

**Desafio**: Validação de campos com tratativas de erros.

**Solução**: Implementação de tratativa de erros

### 👥 Experiência do Usuário

**Desafio**: Criar uma interface para o usuário.

**Solução**: Desenvolvimento de uma interface limpa com CSS, fornecendo feedback claro para ações do usuário, validação de formulários e mensagens de erro informativas.

---

## 🚀 Como Executar

1. Clonar o repositório

   ```
   git clone https://github.com/eliaszlsp/fastapi_p1

2. Criar e Ativar o Ambiente Virtual

   ```
   python -m venv venv
   venv\scripts\activate

3. Instalar os Requerimentos

   ```
   pip install -r requirements.txt

4. Executar o Projeto (Lembre-se de criar o banco de dados 'mydb' antes)

   ```
   uvicorn main:app --reload ou python main.py

---

## 🔌 Endpoints da API

### 📦 Produtos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/produtos` | Lista todos os produtos |
| POST | `/produtos/cadastrar` | Cria novo produto |
| GET | `/produtos/{id}` | Mostra um produto |
| PUT | `/produtos/{id}/editar` | Atualiza produto |
| DELETE | `/produtos/{id}` | Deleta produto |

### 👤 Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/usuarios` | Lista todos os usuários |
| POST | `/usuarios/cadastrar` | Cria novo usuário |
| GET | `/usuarios/{id}` | Mostra um usuário |
| PUT | `/usuarios/{id}/editar` | Atualiza usuário |
| DELETE | `/usuarios/{id}` | Deleta usuário |


###  Testes

Os testes foram realizados com o Swagger UI para verificar:
- Códigos de status HTTP corretos
- Formato e conteúdo das respostas
- Validação de entrada
- Tratamento de erros

### Testes dos Endpoints de Produtos

#### GET /produtos/ - Listar todos os produtos 

O endpoint mostra todos os usuários criados 

![listar_produtos](https://github.com/user-attachments/assets/eca95055-cbed-45e6-9324-be99b598cad4)

#### GET /produtos/{id} - Obter um produto específico

Este endpoint retorna os detalhes de um produto específico com base no ID fornecido.

![encontrar_produto_pelo_id](https://github.com/user-attachments/assets/4b819801-60b0-430b-a763-1cd53ea60416)

#### POST /produtos/cadastrar - Criar um novo produto

Esse endpoint permite a criação de um novo produto com validação de campos.

![cadastrar_novo_produto](https://github.com/user-attachments/assets/d8f48246-ec7c-4de9-a043-4c561af39b9d)

![cadastrar_novo_produto_parte2](https://github.com/user-attachments/assets/234f38d6-c15e-4813-a5da-cf04f266d502)

#### PUT /produtos/{id}/editar - Atualizar um produto

Esse endpoint permite a atualização dos dados de um produto existente.

![put_editar_produto](https://github.com/user-attachments/assets/a7e3311e-253f-42c9-812a-e903efd4198c)

![put_editar_produto2](https://github.com/user-attachments/assets/3fde4167-1d65-48dc-af71-0e44a675ecb1)

#### DELETE /produtos/{id} - Excluir um produto

O endpoint permite a exclusão de um produto do sistema.

![excluir_produto](https://github.com/user-attachments/assets/4179a6cf-3df1-4f92-aa9a-d7fa4c4db31c)

### Testes dos Endpoints de Usuários

#### GET /usuarios - Listar todos os usuários

O endpoint retorna a lista completa de usuários cadastrados no sistema.

![listar_todos_usuarios](https://github.com/user-attachments/assets/f09722de-3a85-41f6-8678-44ebf161b0f3)


#### GET /usuarios/{id} - Obter um usuário específico

O endpoint retorna os detalhes de um usuário específico com base no ID fornecido.

![encontrar_usuario_pelo_id](https://github.com/user-attachments/assets/d3019433-bef2-4495-8313-578e2e8a3a04)

### POST /usuarios/cadastrar - Cadastrar Usuario

O Endpoint permite cadastrar um novo usuário com validação de campos

![cadastrar_novo_usuarios](https://github.com/user-attachments/assets/6259244d-a0ad-4ddb-87e2-3c168f045d3f)

![cadastrar_novo_usuarios_parte2](https://github.com/user-attachments/assets/16875ea3-8607-4d5a-850c-9239ba2448ed)

#### PUT /produtos/{id}/editar - Atualizar um produto

O endpoint edita um usuario já existente

![atualizar_usuario](https://github.com/user-attachments/assets/23bb652a-6145-43d0-a0ea-17fcbce3b361)

![atualizar_usuario_parte2](https://github.com/user-attachments/assets/02017562-d2bb-49cb-84d4-bae8f526be95)

#### DELETE /usuarios/{id} - Excluir um usuário

O endpoint permite excluir um usuário do sistema pelo ID.

![excluir_usuario](https://github.com/user-attachments/assets/90aee2a7-87fb-4a5a-8461-f46b52aee329)

![excluir_usuario_parte2](https://github.com/user-attachments/assets/417e62e6-da1c-4243-b13e-fffe0e41ba89)

### Resultados dos Testes

Todos os endpoints foram testados, demonstrando que a API está funcionando conforme o esperado. Os testes verificaram:

1. **Funcionalidade básica**: Cada endpoint realiza corretamente sua função principal
2. **Validação de dados**: Campos obrigatórios e formatos são validados adequadamente ao editar e cadastrar um produto/usuário
3. **Tratamento de erros**: A API responde apropriadamente a entradas inválidas

### Ferramentas Utilizadas

- **Swagger**: Para testes manuais e documentação da API
- **MySQL**: Banco de dados para ambiente de teste

---

## 📚 Referências

- [Padrão MVC (Model-View-Controller)](https://developer.mozilla.org/en-US/docs/Glossary/MVC)
- [Princípios de Design RESTful](https://restfulapi.net/)
- [Boas Práticas de Segurança Web](https://owasp.org/www-project-top-ten/)
- [Otimização de Desempenho Web](https://web.dev/performance-optimizing-content-efficiency/)
- [Princípios de Usabilidade](https://www.nngroup.com/articles/ten-usability-heuristics/)

---

<table>
  <tr>
      <td align="center">
      <a href="https://github.com/eliaszlsp">
        <img src="https://avatars.githubusercontent.com/u/116045632?v=4" width="100px;" alt="Elias Lopes"/><br />
        <sub><b>Elias Lopes</b></sub>
      </a>
      <br />
    </td>
    <td align="center">
      <a href="https://github.com/Carlos-Leon3l">
        <img src="https://avatars.githubusercontent.com/u/178098701?v=4" width="100px;" alt="Carlos Leonel"/><br />
        <sub><b>Carlos Leonel</b></sub>
      </a>
      <br />
    </td>
  </tr>
</table>
