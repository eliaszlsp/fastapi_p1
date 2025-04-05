# Sistema de Gerenciamento de Produtos e Usuários

## Como executar

1. Configure o banco de dados no arquivo `config.py`
2. Execute o script SQL: `database_setup.sql`
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute a aplicação: `python run.py`

## Endpoints

### Produtos
- GET `/produtos` - Lista todos os produtos
- POST `/produtos/cadastrar` - Cria novo produto
- GET `/produtos/{id}` - Mostra um produto
- POST `/produtos/{id}/editar` - Atualiza produto
- POST `/produtos/{id}` - Deleta produto

### Usuários
- GET `/usuarios` - Lista todos os usuários
- POST `/usuarios/cadastrar` - Cria novo usuário
- GET `/usuarios/{id}` - Mostra um usuário
- POST `/usuarios/{id}/editar` - Atualiza usuário
- POST `/usuarios/{id}` - Deleta usuário
